from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/ws", tags=["realtime"])


def _verify_ws_token(token: str | None) -> dict[str, Any] | None:
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        return None

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return {
            "user_id": user.id,
            "role": "admin" if user.is_admin else payload.get("role", "farmer"),
            "district": payload.get("district"),
            "language": user.language,
        }
    finally:
        db.close()


def _orchestrator(websocket: WebSocket):
    orchestrator = getattr(websocket.app.state, "orchestrator", None)
    if orchestrator is None:
        from app.core.background_tasks import orchestrator as fallback_orchestrator

        orchestrator = fallback_orchestrator
    return orchestrator


async def _send_snapshot(websocket: WebSocket, context: dict[str, Any]) -> None:
    orchestrator = _orchestrator(websocket)
    district = context.get("district")
    snapshot = orchestrator.weather_service.latest_snapshot(district) if district else None
    await websocket.send_json(
        {
            "type": "connected",
            "conn_id": f"user:{context['user_id']}",
            "role": context["role"],
            "district": district,
            "weather": snapshot,
        }
    )


@router.websocket("/farmer")
async def farmer_ws(websocket: WebSocket):
    context = _verify_ws_token(websocket.query_params.get("token"))
    if not context:
        await websocket.close(code=1008)
        return

    orchestrator = _orchestrator(websocket)
    await orchestrator.manager.connect(
        websocket,
        f"user:{context['user_id']}",
        info=orchestrator.manager.get_info(websocket),
    )
    orchestrator.manager.update(websocket, user_id=context["user_id"], role="farmer", district=context.get("district"))
    await _send_snapshot(websocket, context)

    try:
        while True:
            message = await websocket.receive_json()
            action = message.get("action")

            if action == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            if action == "subscribe_weather":
                district = str(message.get("district") or context.get("district") or "pune")
                orchestrator.manager.update(websocket, district=district)
                orchestrator.manager.add_room(websocket, f"district:{district.lower().strip()}")
                snapshot = await orchestrator.weather_service.refresh_district(district)
                await websocket.send_json(snapshot)
                continue

            if action == "predict":
                inputs = message.get("inputs") or {}
                result = await asyncio.to_thread(orchestrator.prediction_service.predict, inputs, context["user_id"], context.get("district"))
                await websocket.send_json(result)
                await orchestrator.manager.broadcast(
                    "admin",
                    {
                        "type": "live_event",
                        "category": "prediction",
                        "user_id": context["user_id"],
                        "district": context.get("district"),
                        "result": result["result"],
                    },
                )
                continue

            if action == "check_pests":
                district = orchestrator.manager.get_info(websocket).district or context.get("district") or "pune"
                snapshot = orchestrator.weather_service.latest_snapshot(district)
                if snapshot is None:
                    snapshot = await orchestrator.weather_service.refresh_district(district)
                alerts = await orchestrator.pest_service.broadcast(snapshot, crop_filter=message.get("crops") or [])
                await websocket.send_json({"type": "pest_alert", "district": district, "alerts": alerts})
                continue

            await websocket.send_json({"type": "error", "message": "Unsupported farmer action"})
    except WebSocketDisconnect:
        orchestrator.manager.disconnect(websocket)
    except Exception:
        orchestrator.manager.disconnect(websocket)
        await websocket.close(code=1011)


@router.websocket("/admin")
async def admin_ws(websocket: WebSocket):
    context = _verify_ws_token(websocket.query_params.get("token"))
    if not context or context["role"] != "admin":
        await websocket.close(code=1008)
        return

    orchestrator = _orchestrator(websocket)
    await orchestrator.manager.connect(websocket, "admin", info=orchestrator.manager.get_info(websocket))
    orchestrator.manager.update(websocket, user_id=context["user_id"], role="admin")
    await websocket.send_json({"type": "connected", "conn_id": f"admin:{context['user_id']}", "role": "admin"})
    await websocket.send_json(orchestrator.admin_service.snapshot())

    try:
        while True:
            message = await websocket.receive_json()
            action = message.get("action")

            if action == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            if action == "get_snapshot":
                await websocket.send_json(orchestrator.admin_service.snapshot())
                continue

            if action == "broadcast_alert":
                district = str(message.get("district") or "unknown")
                alert = {
                    "type": "admin_event",
                    "category": "broadcast_alert",
                    "district": district,
                    "message": message.get("message") or "Admin broadcast",
                }
                await orchestrator.manager.broadcast(f"district:{district.lower().strip()}", alert)
                await orchestrator.manager.broadcast("admin", alert)
                orchestrator.admin_service.record_event("admin_broadcast", {"district": district, "message": alert["message"]})
                continue

            await websocket.send_json({"type": "error", "message": "Unsupported admin action"})
    except WebSocketDisconnect:
        orchestrator.manager.disconnect(websocket)
    except Exception:
        orchestrator.manager.disconnect(websocket)
        await websocket.close(code=1011)

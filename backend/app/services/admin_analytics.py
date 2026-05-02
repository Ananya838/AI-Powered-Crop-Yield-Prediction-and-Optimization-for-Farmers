from __future__ import annotations

import asyncio
from collections import Counter, deque
from datetime import datetime, timezone
from typing import Any


class AdminLiveAnalyticsService:
    def __init__(self, manager) -> None:
        self.manager = manager
        self._running = False
        self._event_log: deque[dict[str, Any]] = deque(maxlen=500)
        self._task: asyncio.Task | None = None

    def record_event(self, event_type: str, payload: dict[str, Any]) -> None:
        event = {
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload,
        }
        self._event_log.append(event)

    def snapshot(self) -> dict[str, Any]:
        recent = list(self._event_log)
        districts = Counter(item.get("district", "unknown") for item in recent if item.get("district"))
        critical = [item for item in recent if item.get("severity") in {"critical", "high"}]
        return {
            "type": "admin_snapshot",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "active_events": len(recent),
            "districts": districts.most_common(5),
            "critical_alerts": critical[-5:],
            "recent_events": recent[-10:],
        }

    async def run_forever(self) -> None:
        self._running = True
        while self._running:
            await self.manager.broadcast("admin", self.snapshot())
            await asyncio.sleep(30)

    async def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.ml.model_loader import explain_prediction
from app.services.prediction_service import generate_yield_forecast


class RealTimePredictionService:
    def __init__(self, admin_service) -> None:
        self.admin_service = admin_service

    def predict(self, inputs: dict[str, Any], user_id: int | None = None, district: str | None = None) -> dict[str, Any]:
        prediction = generate_yield_forecast(inputs)
        prediction["explainability"] = explain_prediction(inputs)
        event = {
            "type": "yield_prediction",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "district": district,
            "result": prediction,
        }
        self.admin_service.record_event("live_prediction", {"district": district or "unknown", "user_id": user_id or 0})
        return event

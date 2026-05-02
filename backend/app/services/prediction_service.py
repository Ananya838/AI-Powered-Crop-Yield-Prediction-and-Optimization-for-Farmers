from __future__ import annotations

from app.ml.model_loader import predict_yield


def generate_yield_forecast(features: dict) -> dict:
    predicted_yield, confidence = predict_yield(features)

    trend = [
        {"year": 2022, "yield": round(predicted_yield * 0.90, 2)},
        {"year": 2023, "yield": round(predicted_yield * 0.95, 2)},
        {"year": 2024, "yield": round(predicted_yield * 1.00, 2)},
        {"year": 2025, "yield": round(predicted_yield * 1.05, 2)},
    ]

    suggested_crop = "millet" if features["rainfall"] < 600 else "paddy"
    return {
        "expected_yield": round(predicted_yield, 2),
        "confidence_score": round(confidence, 2),
        "suggested_crop": suggested_crop,
        "yield_trend": trend,
    }

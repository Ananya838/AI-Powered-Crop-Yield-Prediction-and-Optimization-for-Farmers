from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np

from app.core.config import settings

FEATURE_ORDER = ["rainfall", "temperature", "nitrogen", "phosphorus", "potassium", "ph"]


def _feature_vector(features: dict) -> np.ndarray:
    return np.array([[features.get(key, 0) for key in FEATURE_ORDER]])


def _fallback_predict(features: dict) -> tuple[float, float]:
    base = (
        0.003 * features.get("rainfall", 0)
        + 0.08 * features.get("nitrogen", 0)
        + 0.06 * features.get("phosphorus", 0)
        + 0.05 * features.get("potassium", 0)
        - abs(features.get("ph", 7) - 6.5) * 0.8
    )
    return max(0.8, base), 0.74


def predict_yield(features: dict) -> tuple[float, float]:
    model_path = Path(settings.ml_model_path)
    if model_path.exists():
        model = joblib.load(model_path)
        vector = _feature_vector(features)
        prediction = float(model.predict(vector)[0])
        return prediction, 0.86

    return _fallback_predict(features)


def explain_prediction(features: dict) -> list[dict]:
    model_path = Path(settings.ml_model_path)
    vector = _feature_vector(features)

    if model_path.exists():
        model = joblib.load(model_path)
        try:
            import shap

            explainer = shap.Explainer(model)
            shap_values = explainer(vector)
            values = shap_values.values[0].tolist()
            result = [
                {
                    "feature": feature,
                    "impact": round(float(value), 4),
                    "direction": "positive" if value >= 0 else "negative",
                }
                for feature, value in zip(FEATURE_ORDER, values)
            ]
            return sorted(result, key=lambda item: abs(item["impact"]), reverse=True)
        except Exception:
            pass

    # Fallback pseudo-contribution map when model/SHAP artifacts are unavailable.
    weighted = {
        "rainfall": features.get("rainfall", 0) * 0.003,
        "temperature": -abs(features.get("temperature", 0) - 27) * 0.05,
        "nitrogen": features.get("nitrogen", 0) * 0.08,
        "phosphorus": features.get("phosphorus", 0) * 0.06,
        "potassium": features.get("potassium", 0) * 0.05,
        "ph": -abs(features.get("ph", 7) - 6.5) * 0.8,
    }
    result = [
        {
            "feature": feature,
            "impact": round(float(score), 4),
            "direction": "positive" if score >= 0 else "negative",
        }
        for feature, score in weighted.items()
    ]
    return sorted(result, key=lambda item: abs(item["impact"]), reverse=True)

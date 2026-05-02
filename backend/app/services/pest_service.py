from __future__ import annotations


def assess_pest_risk(crop: str, humidity: float, temperature: float) -> dict:
    score = min(1.0, (humidity / 100.0) * 0.6 + (temperature / 45.0) * 0.4)
    if score < 0.35:
        level = "low"
    elif score < 0.65:
        level = "medium"
    else:
        level = "high"

    return {
        "crop": crop,
        "risk_level": level,
        "risk_score": round(score, 2),
        "advisory": "Spray preventive bio-pesticide and monitor infestation hotspots.",
    }

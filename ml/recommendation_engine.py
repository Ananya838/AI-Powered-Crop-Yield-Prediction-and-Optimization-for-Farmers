from __future__ import annotations


def hybrid_recommendation(payload: dict, predicted_yield: float, pest_risk: str) -> dict:
    rules = []

    if payload["ph"] < 6.0:
        rules.append("Apply lime at 200 kg/hectare to correct acidic soil")
    elif payload["ph"] > 7.5:
        rules.append("Apply gypsum for alkaline correction")

    if payload["rainfall"] < 500:
        rules.append("Adopt drip irrigation with mulching")

    if pest_risk == "high":
        rules.append("Increase scouting frequency and use pheromone traps")

    uplift = 10.0
    if len(rules) >= 3:
        uplift = 14.0
    elif len(rules) == 2:
        uplift = 12.0

    return {
        "base_predicted_yield": predicted_yield,
        "recommended_actions": rules,
        "projected_uplift_percent": uplift,
        "projected_yield": round(predicted_yield * (1 + uplift / 100), 2),
    }


if __name__ == "__main__":
    sample = {
        "ph": 5.8,
        "rainfall": 420,
    }
    print(hybrid_recommendation(sample, predicted_yield=3.1, pest_risk="high"))

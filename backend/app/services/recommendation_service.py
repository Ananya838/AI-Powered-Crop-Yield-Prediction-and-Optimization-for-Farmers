from __future__ import annotations


def build_optimization_plan(payload: dict) -> dict:
    rainfall = payload.get("rainfall", 0)
    irrigation = payload.get("irrigation", "limited")

    irrigation_schedule = [
        "Irrigate every 5 days during vegetative stage",
        "Switch to every 3 days during flowering stage" if rainfall < 500 else "Irrigate every 6 days with rainfall support",
        f"Use {irrigation} infrastructure for targeted watering",
    ]

    fertilizer_dosage = [
        "Basal: NPK 40:20:20 kg/acre",
        "Top dressing at day 30: Urea 25 kg/acre",
        "Micronutrient spray at day 45",
    ]

    return {
        "irrigation_schedule": irrigation_schedule,
        "fertilizer_dosage": fertilizer_dosage,
        "sowing_date": "Within next 7-10 days",
        "harvest_window": "110-125 days after sowing",
        "pest_prevention": [
            "Install pheromone traps",
            "Field scouting twice a week",
            "Use neem-based bio-pesticide in early stage",
        ],
        "disease_risk_alerts": [
            "Moderate fungal risk due to humidity",
            "Monitor leaf spot symptoms after rainfall",
        ],
        "crop_rotation_advice": "Rotate with legumes in next season to restore soil nitrogen.",
        "expected_gain_percent": 12.5,
    }

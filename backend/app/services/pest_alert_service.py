from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.cache import redis_client


PEST_RULES = [
    {
        "id": "fungal_blight",
        "name": "Fungal Blight Risk",
        "severity": "critical",
        "affected_crops": ["tomato", "potato", "chilli"],
        "condition": lambda weather: weather["humidity_pct"] >= 85 and 18 <= weather["temperature_c"] <= 28,
        "action": "Improve airflow and follow preventive fungicide guidance.",
    },
    {
        "id": "powdery_mildew",
        "name": "Powdery Mildew Risk",
        "severity": "high",
        "affected_crops": ["grape", "cucumber", "pumpkin"],
        "condition": lambda weather: weather["humidity_pct"] >= 70 and weather["temperature_c"] >= 24,
        "action": "Reduce leaf wetness and avoid overhead irrigation.",
    },
    {
        "id": "stem_borer",
        "name": "Stem Borer Pressure",
        "severity": "high",
        "affected_crops": ["rice", "sugarcane", "maize"],
        "condition": lambda weather: weather["temperature_c"] >= 30 and weather["rainfall_mm"] >= 5,
        "action": "Inspect field edges and use crop-specific control measures.",
    },
    {
        "id": "aphid_surge",
        "name": "Aphid Surge",
        "severity": "medium",
        "affected_crops": ["mustard", "cotton", "wheat"],
        "condition": lambda weather: 18 <= weather["temperature_c"] <= 32 and weather["humidity_pct"] >= 60,
        "action": "Monitor undersides of leaves and deploy traps early.",
    },
    {
        "id": "mite_pressure",
        "name": "Mite Pressure",
        "severity": "medium",
        "affected_crops": ["cotton", "chilli", "brinjal"],
        "condition": lambda weather: weather["temperature_c"] >= 32 and weather["humidity_pct"] <= 55,
        "action": "Increase scouting and avoid drought stress.",
    },
    {
        "id": "leaf_rust",
        "name": "Leaf Rust Risk",
        "severity": "high",
        "affected_crops": ["wheat", "barley"],
        "condition": lambda weather: 18 <= weather["temperature_c"] <= 26 and weather["humidity_pct"] >= 75,
        "action": "Use resistant varieties and inspect for early lesions.",
    },
    {
        "id": "hopper_blast",
        "name": "Leaf Hopper Risk",
        "severity": "high",
        "affected_crops": ["rice", "cotton"],
        "condition": lambda weather: weather["humidity_pct"] >= 70 and weather["rainfall_mm"] >= 8,
        "action": "Inspect tillers and manage nitrogen carefully.",
    },
    {
        "id": "heat_stress",
        "name": "Heat Stress",
        "severity": "high",
        "affected_crops": ["wheat", "maize", "rice", "cotton"],
        "condition": lambda weather: weather["temperature_c"] >= 35,
        "action": "Increase irrigation priority and reduce fertilizer stress.",
    },
    {
        "id": "water_stress",
        "name": "Water Stress",
        "severity": "critical",
        "affected_crops": ["wheat", "rice", "maize", "soybean"],
        "condition": lambda weather: weather["rainfall_mm"] <= 2 and weather["temperature_c"] >= 30,
        "action": "Schedule irrigation immediately and protect moisture.",
    },
    {
        "id": "storm_damage",
        "name": "Storm Damage Risk",
        "severity": "medium",
        "affected_crops": ["banana", "maize", "sugarcane"],
        "condition": lambda weather: weather["rainfall_mm"] >= 25,
        "action": "Secure supports and avoid field operations during heavy rain.",
    },
]


class PestAlertService:
    def __init__(self, manager, admin_service) -> None:
        self.manager = manager
        self.admin_service = admin_service

    def evaluate(self, weather: dict[str, Any], crop_filter: list[str] | None = None) -> list[dict[str, Any]]:
        crops = {item.lower() for item in (crop_filter or []) if item}
        alerts: list[dict[str, Any]] = []

        for rule in PEST_RULES:
            if crops and not crops.intersection(rule["affected_crops"]):
                continue
            try:
                if rule["condition"](weather):
                    alerts.append(
                        {
                            "rule_id": rule["id"],
                            "name": rule["name"],
                            "severity": rule["severity"],
                            "action": rule["action"],
                            "affected_crops": rule["affected_crops"],
                            "district": weather.get("district"),
                            "generated_at": datetime.now(timezone.utc).isoformat(),
                        }
                    )
            except Exception:
                continue

        return alerts

    def _dedup_key(self, district: str, rule_id: str) -> str:
        return f"pest_sent:{district.lower().strip()}:{rule_id}"

    async def broadcast(self, weather: dict[str, Any], crop_filter: list[str] | None = None) -> list[dict[str, Any]]:
        alerts = self.evaluate(weather, crop_filter=crop_filter)
        district = (weather.get("district") or "unknown").lower().strip()
        fresh_alerts: list[dict[str, Any]] = []

        for alert in alerts:
            cache_key = self._dedup_key(district, alert["rule_id"])
            try:
                if redis_client.get(cache_key):
                    continue
                redis_client.setex(cache_key, 60 * 60, "1")
            except Exception:
                pass
            fresh_alerts.append(alert)

        if fresh_alerts:
            payload = {
                "type": "pest_alert",
                "district": weather.get("district"),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "alerts": fresh_alerts,
            }
            await self.manager.broadcast(f"district:{district}", payload)
            await self.manager.broadcast("admin", {"type": "admin_event", "category": "pest", "district": weather.get("district"), "alerts": fresh_alerts})
            self.admin_service.record_event(
                "critical_pest" if any(alert["severity"] in {"critical", "high"} for alert in fresh_alerts) else "pest_alert",
                {"district": weather.get("district") or "unknown", "severity": fresh_alerts[0]["severity"], "alerts": fresh_alerts},
            )

        return fresh_alerts

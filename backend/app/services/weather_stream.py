from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from statistics import mean
from typing import Any

import httpx


DISTRICT_COORDS = {
    "pune": (18.5204, 73.8567),
    "nashik": (19.9975, 73.7898),
    "nagpur": (21.1458, 79.0882),
    "solapur": (17.6599, 75.9064),
}


def _coords_for_district(district: str) -> tuple[float, float]:
    return DISTRICT_COORDS.get(district.lower().strip(), (20.5937, 78.9629))


class WeatherStreamService:
    def __init__(self, manager, pest_service, admin_service, poll_interval_seconds: int = 600) -> None:
        self.manager = manager
        self.pest_service = pest_service
        self.admin_service = admin_service
        self.poll_interval_seconds = poll_interval_seconds
        self._running = False
        self._latest_snapshots: dict[str, dict[str, Any]] = {}
        self._task: asyncio.Task | None = None

    def latest_snapshot(self, district: str) -> dict[str, Any] | None:
        return self._latest_snapshots.get(district.lower().strip())

    def _build_snapshot(self, district: str) -> dict[str, Any]:
        lat, lon = _coords_for_district(district)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
            "hourly": "temperature_2m,relative_humidity_2m",
            "forecast_days": 7,
            "timezone": "auto",
        }

        rainfall_avg = 0.0
        temp_avg = 0.0
        humidity_avg = 0.0
        source = "fallback"
        forecast_7d: list[dict[str, Any]] = []

        try:
            response = httpx.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            daily = data.get("daily", {})
            hourly = data.get("hourly", {})

            rain_values = daily.get("precipitation_sum", [])
            tmax = daily.get("temperature_2m_max", [])
            tmin = daily.get("temperature_2m_min", [])
            rain_series = rain_values[:7]
            temp_series = [round((x + y) / 2, 2) for x, y in zip(tmax[:7], tmin[:7])]

            rainfall_avg = float(mean(rain_values)) if rain_values else 0.0
            temp_pairs = [(x + y) / 2 for x, y in zip(tmax, tmin)]
            temp_avg = float(mean(temp_pairs)) if temp_pairs else 0.0
            humidity_values = hourly.get("relative_humidity_2m", [])
            humidity_avg = float(mean(humidity_values)) if humidity_values else 0.0
            source = "open-meteo"

            for idx, (day_rain, day_temp) in enumerate(zip(rain_series, temp_series)):
                forecast_7d.append({"day": f"D{idx + 1}", "rainfall_mm": round(float(day_rain), 2), "temperature_c": round(float(day_temp), 2)})
        except Exception:
            fallback_profiles = {
                "kharif": {"rainfall_avg": 12.0, "temp_avg": 28.5, "humidity_avg": 78.0},
                "rabi": {"rainfall_avg": 4.2, "temp_avg": 22.0, "humidity_avg": 64.0},
                "zaid": {"rainfall_avg": 3.0, "temp_avg": 31.0, "humidity_avg": 52.0},
            }
            fallback = fallback_profiles["kharif"]
            rainfall_avg = fallback["rainfall_avg"]
            temp_avg = fallback["temp_avg"]
            humidity_avg = fallback["humidity_avg"]
            forecast_7d = [
                {"day": f"D{idx + 1}", "rainfall_mm": rainfall_avg * 0.9, "temperature_c": temp_avg + (idx % 3) * 0.4}
                for idx in range(7)
            ]

        irrigation_advice = "Maintain standard irrigation schedule"
        if rainfall_avg < 4:
            irrigation_advice = "Increase irrigation frequency and protect topsoil moisture"
        elif rainfall_avg > 15:
            irrigation_advice = "Delay irrigation and improve drainage"

        return {
            "type": "weather_update",
            "district": district,
            "current": {
                "temperature_c": round(temp_avg, 2),
                "humidity_pct": round(humidity_avg, 2),
                "rainfall_mm": round(rainfall_avg, 2),
            },
            "forecast_7d": forecast_7d,
            "irrigation_advice": irrigation_advice,
            "source": source,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }

    async def refresh_district(self, district: str) -> dict[str, Any]:
        snapshot = await asyncio.to_thread(self._build_snapshot, district)
        previous = self._latest_snapshots.get(district.lower().strip())
        self._latest_snapshots[district.lower().strip()] = snapshot

        await self.manager.broadcast(f"district:{district.lower().strip()}", snapshot)

        if previous is None or self._is_significant_change(previous, snapshot):
            await self.manager.broadcast(
                "admin",
                {
                    "type": "admin_event",
                    "category": "weather",
                    "district": district,
                    "current": snapshot["current"],
                    "fetched_at": snapshot["fetched_at"],
                },
            )
            self.admin_service.record_event("weather_change", {"district": district, **snapshot["current"]})
            await self.pest_service.broadcast(snapshot)

        return snapshot

    def _is_significant_change(self, previous: dict[str, Any], current: dict[str, Any]) -> bool:
        prev_current = previous.get("current", {})
        curr_current = current.get("current", {})
        temp_delta = abs(float(curr_current.get("temperature_c", 0)) - float(prev_current.get("temperature_c", 0)))
        humidity_delta = abs(float(curr_current.get("humidity_pct", 0)) - float(prev_current.get("humidity_pct", 0)))
        rain_delta = abs(float(curr_current.get("rainfall_mm", 0)) - float(prev_current.get("rainfall_mm", 0)))
        return temp_delta >= 1.5 or humidity_delta >= 8 or rain_delta >= 4

    async def run_forever(self) -> None:
        self._running = True
        districts = list(DISTRICT_COORDS.keys())
        while self._running:
            for district in districts:
                try:
                    await self.refresh_district(district)
                except Exception:
                    continue
            await asyncio.sleep(self.poll_interval_seconds)

    async def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()

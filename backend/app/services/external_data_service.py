from __future__ import annotations

import json
from statistics import mean

import httpx
from sqlalchemy.orm import Session

from app.core.cache import redis_client
from app.models.weather_cache import WeatherCache

DISTRICT_COORDS = {
    "pune": (18.5204, 73.8567),
    "nashik": (19.9975, 73.7898),
    "nagpur": (21.1458, 79.0882),
    "solapur": (17.6599, 75.9064),
}

# District-level typical soil profiles for farmers who deny location access
DISTRICT_SOIL_PROFILES = {
    "pune": {
        "ph": 6.8,
        "nitrogen": 52.0,
        "estimated_phosphorus": 28.0,
        "estimated_potassium": 210.0,
        "soil_organic_carbon": 7.2,
    },
    "nashik": {
        "ph": 7.1,
        "nitrogen": 48.0,
        "estimated_phosphorus": 25.0,
        "estimated_potassium": 195.0,
        "soil_organic_carbon": 6.8,
    },
    "nagpur": {
        "ph": 6.5,
        "nitrogen": 55.0,
        "estimated_phosphorus": 32.0,
        "estimated_potassium": 225.0,
        "soil_organic_carbon": 8.1,
    },
    "solapur": {
        "ph": 7.2,
        "nitrogen": 45.0,
        "estimated_phosphorus": 22.0,
        "estimated_potassium": 180.0,
        "soil_organic_carbon": 6.0,
    },
}


def _coords_for_district(district: str) -> tuple[float, float]:
    return DISTRICT_COORDS.get(district.lower().strip(), (20.5937, 78.9629))


def fetch_weather_summary(district: str, season: str, db: Session) -> dict:
    cache_key = f"weather:{district.lower()}:{season.lower()}"
    try:
        cached = redis_client.get(cache_key)
        if cached:
            payload = json.loads(cached)
            payload["source"] = "redis"
            return payload
    except Exception:
        cached = None

    lat, lon = _coords_for_district(district)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
        "forecast_days": 14,
        "timezone": "auto",
    }

    source = "open-meteo"
    rainfall_avg = 0.0
    temp_avg = 0.0
    raw_payload = "{}"

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        daily = data.get("daily", {})

        rain_values = daily.get("precipitation_sum", [])
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])

        rainfall_avg = float(mean(rain_values)) if rain_values else 0.0
        temp_pairs = [(x + y) / 2 for x, y in zip(tmax, tmin)]
        temp_avg = float(mean(temp_pairs)) if temp_pairs else 0.0
        raw_payload = json.dumps(data)
    except Exception:
        # Fallback profile ensures service availability in low-connectivity demos.
        source = "fallback"
        if season.lower() == "kharif":
            rainfall_avg = 12.0
            temp_avg = 28.5
        elif season.lower() == "rabi":
            rainfall_avg = 4.2
            temp_avg = 22.0
        else:
            rainfall_avg = 6.5
            temp_avg = 26.0

    db.add(
        WeatherCache(
            district=district,
            season=season,
            avg_rainfall_mm=rainfall_avg,
            avg_temperature_c=temp_avg,
            raw_payload=raw_payload,
        )
    )
    db.commit()

    payload = {
        "district": district,
        "season": season,
        "avg_rainfall_mm": round(rainfall_avg, 2),
        "avg_temperature_c": round(temp_avg, 2),
        "source": source,
    }
    try:
        redis_client.setex(cache_key, 6 * 60 * 60, json.dumps(payload))
    except Exception:
        pass
    return payload


def fetch_soil_by_district(district: str) -> dict:
    """Fetch typical soil profile for a district (fallback when geolocation unavailable)."""
    profile = DISTRICT_SOIL_PROFILES.get(district.lower().strip())
    if profile:
        return {
            "district": district,
            "ph": profile["ph"],
            "nitrogen": profile["nitrogen"],
            "estimated_phosphorus": profile["estimated_phosphorus"],
            "estimated_potassium": profile["estimated_potassium"],
            "soil_organic_carbon": profile["soil_organic_carbon"],
            "source": "district_profile",
        }
    # Default fallback if district not in map
    return {
        "district": district,
        "ph": 6.5,
        "nitrogen": 50.0,
        "estimated_phosphorus": 28.0,
        "estimated_potassium": 210.0,
        "soil_organic_carbon": 7.5,
        "source": "default_fallback",
    }


def fetch_soil_summary(latitude: float, longitude: float) -> dict:
    url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    params = {
        "lat": latitude,
        "lon": longitude,
        "property": ["nitrogen", "phh2o", "soc"],
        "depth": ["0-5cm"],
        "value": ["mean"],
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        layers = data.get("properties", {}).get("layers", [])
        mapped = {layer.get("name"): layer for layer in layers}

        def _extract(layer_name: str, default: float) -> float:
            layer = mapped.get(layer_name, {})
            depths = layer.get("depths", [])
            if not depths:
                return default
            values = depths[0].get("values", {})
            return float(values.get("mean", default))

        nitrogen_value = round(_extract("nitrogen", 45.0), 2)
        ph_value = round(_extract("phh2o", 62.0) / 10, 2)
        soc_value = round(_extract("soc", 7.5), 2)

        # Heuristic conversion for demo-supporting NPK completion when lab values are unavailable.
        estimated_phosphorus = round(max(10.0, min(80.0, nitrogen_value * 0.48 + soc_value * 0.9)), 2)
        estimated_potassium = round(max(10.0, min(90.0, nitrogen_value * 0.42 + soc_value * 1.2)), 2)

        return {
            "latitude": latitude,
            "longitude": longitude,
            "ph": ph_value,
            "nitrogen": nitrogen_value,
            "estimated_phosphorus": estimated_phosphorus,
            "estimated_potassium": estimated_potassium,
            "soil_organic_carbon": soc_value,
            "source": "soilgrids",
        }
    except Exception:
        return {
            "latitude": latitude,
            "longitude": longitude,
            "ph": 6.4,
            "nitrogen": 48.0,
            "estimated_phosphorus": 30.0,
            "estimated_potassium": 24.0,
            "soil_organic_carbon": 8.1,
            "source": "fallback",
        }

from pydantic import BaseModel


class WeatherSummaryResponse(BaseModel):
    district: str
    season: str
    avg_rainfall_mm: float
    avg_temperature_c: float
    source: str


class SoilSummaryResponse(BaseModel):
    latitude: float
    longitude: float
    ph: float
    nitrogen: float
    estimated_phosphorus: float
    estimated_potassium: float
    soil_organic_carbon: float
    source: str

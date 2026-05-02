from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.data_sources import SoilSummaryResponse, WeatherSummaryResponse
from app.services.external_data_service import fetch_soil_summary, fetch_soil_by_district, fetch_weather_summary

router = APIRouter(prefix="/data", tags=["data-sources"])


@router.get("/weather", response_model=WeatherSummaryResponse)
def weather_data(
    district: str,
    season: str,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return fetch_weather_summary(district=district, season=season, db=db)


@router.get("/soil", response_model=SoilSummaryResponse)
def soil_data(
    latitude: float,
    longitude: float,
    _: User = Depends(get_current_user),
):
    return fetch_soil_summary(latitude=latitude, longitude=longitude)


@router.get("/soil-by-district", response_model=SoilSummaryResponse)
def soil_data_by_district(
    district: str,
    _: User = Depends(get_current_user),
):
    """Fetch typical soil profile for a district (fallback when geolocation unavailable)."""
    return fetch_soil_by_district(district=district)

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, func

from app.core.database import Base


class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String(80), nullable=False, index=True)
    season = Column(String(30), nullable=False)
    avg_rainfall_mm = Column(Float, nullable=False)
    avg_temperature_c = Column(Float, nullable=False)
    raw_payload = Column(Text, nullable=True)
    fetched_at = Column(DateTime, server_default=func.now(), nullable=False)

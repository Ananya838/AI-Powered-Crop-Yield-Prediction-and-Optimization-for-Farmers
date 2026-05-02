from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.core.database import Base


class CropHistory(Base):
    __tablename__ = "crop_history"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String(80), nullable=False)
    crop = Column(String(80), nullable=False)
    season = Column(String(30), nullable=False)
    yield_per_hectare = Column(Float, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

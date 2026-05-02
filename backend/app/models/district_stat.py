from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.core.database import Base


class DistrictStat(Base):
    __tablename__ = "district_stats"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String(80), unique=True, nullable=False)
    avg_productivity = Column(Float, nullable=False)
    adoption_rate = Column(Float, nullable=False)
    failure_alert_count = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, func

from app.core.database import Base


class PestAlert(Base):
    __tablename__ = "pest_alerts"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String(80), nullable=False)
    crop = Column(String(80), nullable=False)
    risk_level = Column(String(20), nullable=False)
    risk_score = Column(Float, nullable=False)
    advisory = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

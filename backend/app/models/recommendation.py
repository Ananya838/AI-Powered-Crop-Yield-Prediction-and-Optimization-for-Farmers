from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func

from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    irrigation_schedule = Column(Text, nullable=False)
    fertilizer_dosage = Column(Text, nullable=False)
    sowing_date = Column(String(30), nullable=False)
    harvest_window = Column(String(30), nullable=False)
    rotation_advice = Column(Text, nullable=True)
    expected_gain_percent = Column(Float, default=10.0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

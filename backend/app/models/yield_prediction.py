from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func

from app.core.database import Base


class YieldPrediction(Base):
    __tablename__ = "yield_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    crop = Column(String(80), nullable=False)
    season = Column(String(30), nullable=False)
    predicted_yield = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    suggested_crop = Column(String(80), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

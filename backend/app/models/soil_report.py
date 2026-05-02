from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, func

from app.core.database import Base


class SoilReport(Base):
    __tablename__ = "soil_reports"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    nitrogen = Column(Float, nullable=False)
    phosphorus = Column(Float, nullable=False)
    potassium = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    organic_carbon = Column(Float, nullable=True)
    moisture = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

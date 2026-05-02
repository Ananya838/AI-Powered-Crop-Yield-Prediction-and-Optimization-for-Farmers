from pydantic import BaseModel


class OptimizationPlanResponse(BaseModel):
    irrigation_schedule: list[str]
    fertilizer_dosage: list[str]
    sowing_date: str
    harvest_window: str
    pest_prevention: list[str]
    disease_risk_alerts: list[str]
    crop_rotation_advice: str
    expected_gain_percent: float

from pydantic import BaseModel, Field


class YieldPredictionRequest(BaseModel):
    crop: str
    district: str
    village: str
    rainfall: float = Field(..., ge=0)
    temperature: float
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    irrigation: str
    season: str


class YieldPredictionResponse(BaseModel):
    expected_yield: float
    confidence_score: float
    suggested_crop: str
    yield_trend: list[dict]
    explainability: list[dict]

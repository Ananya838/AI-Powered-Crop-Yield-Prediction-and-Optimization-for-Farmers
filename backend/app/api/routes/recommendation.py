from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.prediction import YieldPredictionRequest
from app.schemas.recommendation import OptimizationPlanResponse
from app.services.recommendation_service import build_optimization_plan

router = APIRouter(prefix="/optimization", tags=["optimization"])


@router.post("/plan", response_model=OptimizationPlanResponse)
def optimization_plan(payload: YieldPredictionRequest, current_user: User = Depends(get_current_user)):
    _ = current_user
    return build_optimization_plan(payload.model_dump())

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.ml.model_loader import explain_prediction
from app.models.user import User
from app.models.yield_prediction import YieldPrediction
from app.schemas.prediction import YieldPredictionRequest, YieldPredictionResponse
from app.services.prediction_service import generate_yield_forecast

router = APIRouter(prefix="/prediction", tags=["prediction"])


@router.post("/yield", response_model=YieldPredictionResponse)
def predict_yield(
    payload: YieldPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = generate_yield_forecast(payload.model_dump())
    result["explainability"] = explain_prediction(payload.model_dump())
    row = YieldPrediction(
        user_id=current_user.id,
        crop=payload.crop,
        season=payload.season,
        predicted_yield=result["expected_yield"],
        confidence_score=result["confidence_score"],
        suggested_crop=result["suggested_crop"],
    )
    db.add(row)
    db.commit()
    return result


@router.post("/explain")
def explain_yield(
    payload: YieldPredictionRequest,
    _: User = Depends(get_current_user),
):
    return {"explainability": explain_prediction(payload.model_dump())}

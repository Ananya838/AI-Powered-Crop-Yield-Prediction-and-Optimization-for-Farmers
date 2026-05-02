from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.services.pest_service import assess_pest_risk

router = APIRouter(prefix="/pest", tags=["pest"])


@router.get("/risk")
def pest_risk(crop: str, humidity: float, temperature: float, current_user: User = Depends(get_current_user)):
    _ = current_user
    return assess_pest_risk(crop=crop, humidity=humidity, temperature=temperature)

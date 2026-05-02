from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.farm import Farm
from app.models.user import User

router = APIRouter(prefix="/farms", tags=["farms"])


@router.get("")
def list_farms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Farm).filter(Farm.user_id == current_user.id).all()

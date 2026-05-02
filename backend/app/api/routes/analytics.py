from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.schemas.analytics import AdminAnalyticsResponse
from app.services.analytics_service import admin_analytics_snapshot

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/analytics", response_model=AdminAnalyticsResponse)
def analytics(_=Depends(get_current_admin), db: Session = Depends(get_db)):
    return admin_analytics_snapshot(db)

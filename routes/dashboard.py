from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.dashboard_service import (
    get_summary, get_category_wise,
    get_monthly_trends, get_recent_activity
)
from core.dependencies import require_analyst_or_admin, require_any
from models.user import User
from schemas.record import RecordResponse
from typing import List

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any)
):
    """Get total income, expense and net balance - All roles"""
    return get_summary(db)

@router.get("/category-wise")
def category_wise(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin)
):
    """Get category wise breakdown - Analyst and Admin only"""
    return get_category_wise(db)

@router.get("/monthly-trends")
def monthly_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin)
):
    """Get monthly income and expense trends - Analyst and Admin only"""
    return get_monthly_trends(db)

@router.get("/recent-activity", response_model=List[RecordResponse])
def recent_activity(
    limit: int = Query(10, description="Number of recent records to fetch"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any)
):
    """Get recent transactions - All roles"""
    return get_recent_activity(db, limit)
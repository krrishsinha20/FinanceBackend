from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.record import RecordCreate, RecordUpdate, RecordResponse
from services.record_service import (
    create_record, get_all_records,
    get_record_by_id, update_record, delete_record
)
from core.dependencies import require_admin, require_any, require_analyst_or_admin
from models.user import User
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/records", tags=["Financial Records"])

@router.post("/", response_model=RecordResponse)
def create(
    record_data: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new financial record - Admin only"""
    return create_record(db, record_data, current_user.id)

@router.get("/", response_model=List[RecordResponse])
def list_records(
    type: Optional[str] = Query(None, description="Filter by type: income or expense"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[datetime] = Query(None, description="Filter from date"),
    end_date: Optional[datetime] = Query(None, description="Filter to date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any)
):
    """Get all records with optional filters - All roles"""
    return get_all_records(db, type, category, start_date, end_date)

@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any)
):
    """Get single record by ID - All roles"""
    return get_record_by_id(db, record_id)

@router.put("/{record_id}", response_model=RecordResponse)
def update(
    record_id: int,
    record_data: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a record - Admin only"""
    return update_record(db, record_id, record_data)

@router.delete("/{record_id}")
def delete(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a record - Admin only"""
    return delete_record(db, record_id)
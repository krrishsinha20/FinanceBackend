from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.record import RecordCreate, RecordUpdate, RecordResponse
from services.record_service import (
    create_record, get_all_records,
    get_record_by_id, update_record, delete_record
)
from core.dependencies import require_admin, require_any
from models.user import User
from typing import List, Optional
from datetime import datetime

def parse_date(date_str: str, field_name: str) -> datetime:
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    raise HTTPException(
        status_code=400,
        detail=f"Invalid {field_name} format. Use: YYYY-MM-DD or DD-MM-YYYY or DD/MM/YYYY"
    )

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
    type: Optional[str] = Query(None, description="Filter by type: income or expense. Leave empty to see all records"),
    category: Optional[str] = Query(None, description="Filter by category name. Leave empty to see all records"),
    start_date: Optional[str] = Query(None, description="Filter from date. Format: 2026-01-01 or 01-01-2026. Leave empty to see all records"),
    end_date: Optional[str] = Query(None, description="Filter to date. Format: 2026-04-01 or 01-04-2026. Leave empty to see all records"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any)
):
    """Get all records with optional filters. Leave all fields empty to see all records - All roles"""
    parsed_start = parse_date(start_date, "start_date") if start_date else None
    parsed_end = parse_date(end_date, "end_date") if end_date else None
    return get_all_records(db, type, category, parsed_start, parsed_end)

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
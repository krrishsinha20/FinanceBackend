from sqlalchemy.orm import Session
from models.record import FinancialRecord
from schemas.record import RecordCreate, RecordUpdate
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional

def create_record(db: Session, record_data: RecordCreate, user_id: int):
    new_record = FinancialRecord(
        amount=record_data.amount,
        type=record_data.type,
        category=record_data.category,
        date=record_data.date,
        notes=record_data.notes,
        created_by=user_id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def get_all_records(
    db: Session,
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    )

    if type:
        query = query.filter(FinancialRecord.type == type)
    if category:
        query = query.filter(FinancialRecord.category == category)
    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)

    records = query.order_by(FinancialRecord.date.desc()).all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No records found for the given filters"
        )
    return records

def get_record_by_id(db: Session, record_id: int):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    return record

def update_record(db: Session, record_id: int, record_data: RecordUpdate):
    record = get_record_by_id(db, record_id)

    if record_data.amount is not None:
        if record_data.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be greater than 0"
            )
        record.amount = record_data.amount
    if record_data.type is not None:
        if record_data.type not in ["income", "expense"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type must be income or expense"
            )
        record.type = record_data.type
    if record_data.category is not None:
        record.category = record_data.category
    if record_data.date is not None:
        record.date = record_data.date
    if record_data.notes is not None:
        record.notes = record_data.notes

    db.commit()
    db.refresh(record)
    return record

def delete_record(db: Session, record_id: int):
    record = get_record_by_id(db, record_id)
    record.is_deleted = True  # soft delete
    db.commit()
    return {"message": "Record deleted successfully"}
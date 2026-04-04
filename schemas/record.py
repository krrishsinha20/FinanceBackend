from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: datetime
    notes: Optional[str] = None

    @field_validator("amount", mode="before")
    @classmethod
    def amount_must_be_valid(cls, v):
        try:
            v = float(str(v).lstrip("0") or "0")
        except:
            raise ValueError("Amount must be a valid number")
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2)

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, v):
        if v not in ["income", "expense"]:
            raise ValueError("type must be 'income' or 'expense'")
        return v

    @field_validator("category")
    @classmethod
    def category_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip()

    @field_validator("date", mode="before")
    @classmethod
    def date_must_be_valid(cls, v):
        if isinstance(v, datetime):
            parsed = v
        else:
            formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%d/%m/%Y",
            ]
            parsed = None
            for fmt in formats:
                try:
                    parsed = datetime.strptime(str(v), fmt)
                    break
                except:
                    continue
            if parsed is None:
                raise ValueError(
                    "Invalid date. Use formats like: 2026-04-05 or 2026-04-05T10:00:00 or 05-04-2026 or 05/04/2026"
                )

        if parsed.year < 1900:
            raise ValueError("Date year must be after 1900")
        if parsed > datetime.now():
            raise ValueError("Date cannot be in the future")
        return parsed

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator("date", mode="before")
    @classmethod
    def date_must_be_valid(cls, v):
        if v is None:
            return v
        if isinstance(v, datetime):
            parsed = v
        else:
            formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%d/%m/%Y",
            ]
            parsed = None
            for fmt in formats:
                try:
                    parsed = datetime.strptime(str(v), fmt)
                    break
                except:
                    continue
            if parsed is None:
                raise ValueError(
                    "Invalid date. Use formats like: 2026-04-05 or 2026-04-05T10:00:00 or 05-04-2026 or 05/04/2026"
                )
        if parsed.year < 1900:
            raise ValueError("Date year must be after 1900")
        if parsed > datetime.now():
            raise ValueError("Date cannot be in the future")
        return parsed

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: datetime
    notes: Optional[str]
    is_deleted: bool
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
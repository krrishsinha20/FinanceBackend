from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class RecordCreate(BaseModel):
    amount: float
    type: str           # income or expense
    category: str
    date: datetime
    notes: Optional[str] = None

    @validator("type")
    def type_must_be_valid(cls, v):
        if v not in ["income", "expense"]:
            raise ValueError("type must be 'income' or 'expense'")
        return v

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be greater than 0")
        return v

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

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
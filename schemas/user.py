from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "viewer"

    @field_validator("password")
    def password_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("Password cannot be empty or whitespace only")
        if len(v.strip()) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("name")
    def name_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v.strip()

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
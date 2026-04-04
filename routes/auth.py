from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserResponse
from services.auth_service import register_user, login_user


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with name, email, password and role"""
    return register_user(db, user_data)

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    
    """Login with email and password to get JWT token"""
    return login_user(db, username, password)
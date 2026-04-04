from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserResponse, UserUpdate
from services.user_service import get_all_users, get_user_by_id, update_user, delete_user
from core.dependencies import require_admin, get_current_user
from models.user import User
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all users - Admin only"""
    return get_all_users(db)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current logged in user info"""
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get user by ID - Admin only"""
    return get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update user role or status - Admin only"""
    return update_user(db, user_id, user_data, current_user.id)

@router.delete("/{user_id}")
def delete(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Deactivate user - Admin only"""
    return delete_user(db, user_id, current_user.id)
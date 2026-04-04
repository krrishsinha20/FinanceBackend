from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserUpdate
from fastapi import HTTPException, status

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def update_user(db: Session, user_id: int, user_data: UserUpdate, current_user_id: int):
    if user_id == current_user_id and user_data.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account"
        )
    
    user = get_user_by_id(db, user_id)

    if user_data.role and user_data.role not in ["viewer", "analyst", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be viewer, analyst, or admin"
        )

    if user_data.name is not None:
        user.name = user_data.name
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int, current_user_id: int):
    if user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account"
        )
    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}
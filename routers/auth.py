from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth_utils import verify_password, get_password_hash, create_access_token, get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    full_name: Optional[str] = None
    assigned_site: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    role: str
    full_name: Optional[str] = None
    assigned_site: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create users")
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
        role=user.role,
        full_name=user.full_name,
        assigned_site=user.assigned_site
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is disabled")
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "full_name": user.full_name,
        "username": user.username
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "user_id": str(current_user.user_id),
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "full_name": current_user.full_name,
        "assigned_site": current_user.assigned_site
    }

@router.get("/users")
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view all users")
    return db.query(User).all()
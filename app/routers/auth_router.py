from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.auth_schema import TokenResponse , RegisterRequest
from app.services.auth_service import authenticate_user , register_user 
from app.core.auth import get_current_user
from app.models.user import User
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, payload.email, payload.password)
    return {"id": str(user.id), "email": user.email}


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = authenticate_user(
        db,
        email=form_data.username,   # Swagger uses "username"
        password=form_data.password,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }









@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": str(current_user.id), "email": current_user.email}

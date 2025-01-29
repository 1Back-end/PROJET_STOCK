from datetime import timedelta, datetime
from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, get_password_hash
from app.main.core.config import Config

router = APIRouter(prefix="", tags=["users"])

@router.post("/register", response_model=schemas.Msg)
def register(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    exist_phone = crud.user.get_by_email(db=db,email=user_in.email)
    if exist_phone:
        raise HTTPException(status_code=400,detail=__(key="email-already-exists"))
    exist_phone = crud.user.get_by_phone_number(db=db,phone_number=user_in.phone_number)
    if exist_phone:
        raise HTTPException(status_code=400,detail=__(key="phone-number-already-exists"))
    
    crud.user.create(db=db, obj_in=user_in)
    return schemas.Msg(message=__(key="user-created-successfully"))

@router.post("/login", response_model=schemas.UserAuthentification)
def login(
    username: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db),
):
    user = crud.user.authenticate(db=db,username=username,password=password)
    if not user:
        raise HTTPException(status_code=400, detail=__(key="invalid-credentials"))
    if user.status in [models.UserStatus.BLOCKED, models.UserStatus.DELETED]:
        raise HTTPException(status_code=400, detail=__(key="auth-login-failed"))
    if user.status != models.UserStatus.ACTIVED:
        raise HTTPException(status_code=400, detail=__(key="user-not-activated"))
    
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "user": user,
        "token": {
            "access_token": create_access_token(
                user.uuid, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    }
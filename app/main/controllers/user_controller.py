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
async def register(
    db: Session = Depends(get_db),
    *,
    user_in: schemas.UserCreate
):
    exist_phone = crud.user.get_user_by_phone_number(db,phone_number=user_in.phone_number)
    if exist_phone:
        raise HTTPException(status_code=400, detail=__(key="phone-number-already-exists"))
    exist_email = crud.user.get_user_by_email(db, email=user_in.email)
    if exist_email:
        raise HTTPException(status_code=400, detail=__(key="email-already-exists"))
    crud.user.create_user(db=db,user_in=user_in)
    return schemas.Msg(message=__(key="user-registered"))
    
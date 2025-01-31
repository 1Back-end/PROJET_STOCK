from datetime import timedelta, datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, generate_code, get_password_hash
from app.main.core.config import Config
from app.main.core import mail

router = APIRouter(prefix="", tags=["products"])

@router.post("/create",response_model=schemas.ProductResponse)
async def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductCreate,
    current_user: models.User = Depends(TokenRequired())
):
    user_uuid = current_user.uuid
    return crud.product.create_product(db=db,obj_in=obj_in,user_uuid=user_uuid)
from datetime import date, timedelta, datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __

router = APIRouter(prefix="/replenishment",tags=["replenishment"])

@router.post("",response_model=schemas.ResplishmentResponse)
def create(
    *,
    db:Session=Depends(get_db),
    obj_in:schemas.ReplenishmentCreate,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
    user_uuid = current_user.uuid
    return crud.replenishment.create_replenishment(db=db,obj_in=obj_in,user_uuid=user_uuid)
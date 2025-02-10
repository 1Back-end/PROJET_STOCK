from datetime import timedelta, datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, generate_code, get_password_hash
from app.main.core.config import Config
from app.main.core import mail

router = APIRouter(prefix="", tags=["category"])

@router.post("/create", response_model=schemas.Msg)
async def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CategoryCreate,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
    user_uuid = current_user.uuid
    exist_name = crud.category.get_category_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=400, detail=__(key="category-already-exists."))
    crud.category.create_category(db=db,obj_in=obj_in,user_uuid=user_uuid)
    return schemas.Msg(message=__(key="category-created-successfully."))

@router.put("/edit",response_model=schemas.Msg)
async def update(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
   user_uuid = current_user.uuid
   crud.category.update_category(db=db,obj_in=obj_in,user_uuid=user_uuid)
   return schemas.Msg(message=__(key="category-updated-successfully."))


@router.delete("/delete", response_model=schemas.Msg)
async def delete(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.CategoryDelete,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN"]))
):
    user_uuid = current_user.uuid
    crud.category.delete_category(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="category-deleted-successfully."))

@router.get("/get_all", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 20,
    order: str = Query("desc", enum=["asc", "desc"]),
    order_field: str = "date_added",  # Correction de "order_filed" à "order_field"
    keyword: Optional[str] = None,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
    return crud.category.get_many(
        db=db, 
        page=page, 
        per_page=per_page, 
        order=order, 
        order_field=order_field,  # Utilisation du bon nom de variable
        keyword=keyword
    )
@router.get("/list",response_model=List[schemas.CategoryDetails])
async def get_list(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
    return crud.category.get_all_categories(db=db)

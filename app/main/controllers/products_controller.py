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

router = APIRouter(prefix="/products", tags=["products"])

@router.post("",response_model=schemas.ProductResponse)
async def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductCreate,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
    user_uuid = current_user.uuid
    return crud.product.create_product(db=db,obj_in=obj_in,user_uuid=user_uuid)

@router.put("",response_model=schemas.ProductResponse)
async def update(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.ProductUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
   user_uuid = current_user.uuid
   return crud.product.update_product(db=db,obj_in=obj_in,user_uuid=user_uuid)
  
@router.delete("", response_model=schemas.Msg)
async def delete(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.ProductDelete,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN"]))
):
    crud.product.delete_product(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="product-deleted-successfully."))

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
    return crud.product.get_many(
        db=db, 
        page=page, 
        per_page=per_page, 
        order=order, 
        order_field=order_field,  # Utilisation du bon nom de variable
        keyword=keyword
    )

@router.get("/{uuid}", response_model=schemas.ProductResponse)
async def read(
    *,
    db: Session = Depends(get_db),
    uuid: str,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
    return crud.product.get_product_by_uuid(db=db, uuid=uuid)

# @router.get("/{name}",response_model=schemas.ProductResponse)
# async def read_by_name(
#     *,
#     db: Session = Depends(get_db),
#     name: str,
#     current_user: models.User = Depends(TokenRequired())
# ):
#     product= crud.product.get_product_by_name(db=db,name=name)
#     if not product:
#         raise HTTPException(status_code=404, detail=__(key="product-not-found."))
#     return product
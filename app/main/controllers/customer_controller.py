from datetime import timedelta, datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("",response_model=schemas.Msg)
def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CustomerCreate,
    current_user: models.User = Depends(TokenRequired())
):
    exist_phone = crud.customer.get_customer_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone is not None:
        raise HTTPException(status_code=400, detail=__(key="phone-number-already-exists"))
    exist_email = crud.customer.get_customer_by_email(db=db,email=obj_in.email)
    if exist_email is not None:
        raise HTTPException(status_code=400, detail=__(key="email-already-exists"))
    user_uuid=current_user.uuid
    crud.customer.create_customer(db=db,obj_in=obj_in,user_uuid=user_uuid)
    return schemas.Msg(message=__(key="customer-created-successfully."))

@router.put("",response_model=schemas.Msg)
async def update(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.CustomerUpdate,
    current_user: models.User = Depends(TokenRequired())
):
   user_uuid = current_user.uuid
   crud.customer.update_customer(db=db,user_in=user_in,user_uuid=user_uuid)
   return schemas.Msg(message=__(key="customer-update-successfully"))

  
@router.delete("",response_model=schemas.Msg)
async def delete(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.CustomerDelete,
    current_user: models.User = Depends(TokenRequired())
):
    crud.customer.delete_customer(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key='customer-deleted-successfully'))

@router.get("/{uuid}",response_model=schemas.CustomerResponse)
async def read(
    *,
    db: Session = Depends(get_db),
    uuid: str,
    current_user: models.User = Depends(TokenRequired())
):
    return crud.customer.get_customer_by_uuid(db=db, uuid=uuid)

@router.get("", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 20,
    order: str = Query("desc", enum=["asc", "desc"]),
    order_field: str = "date_added",  # Correction de "order_filed" à "order_field"
    keyword: Optional[str] = None,
    current_user: models.User = Depends(TokenRequired())
):
    return crud.customer.get_many(
        db=db, 
        page=page, 
        per_page=per_page, 
        order=order, 
        order_field=order_field,  # Utilisation du bon nom de variable
        keyword=keyword
    )

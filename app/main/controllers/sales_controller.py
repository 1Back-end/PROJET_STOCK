from datetime import date, timedelta, datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, generate_code, get_password_hash
from app.main.core.config import Config


router = APIRouter(prefix="/sales",tags=["sales"])



@router.post("",response_model=schemas.Msg)
async def create(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SalesCreate,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"])),
):
    user_uuid = current_user.uuid
    crud.sales.create_sales(db=db,obj_in=obj_in,user_uuid=user_uuid)
    return {"message": __(key="sales-created-successfully")}


@router.get("/{customer_uuid}",response_model=List[schemas.SalesResponseSlim1])
async def read_sales_by_customer(
    *,
    db: Session = Depends(get_db),
    customer_uuid: str,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"])),
):
    return crud.sales.get_sales_by_customer(db=db, customer_uuid=customer_uuid)

@router.put("",response_model=schemas.Msg)
async def update(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.SalesUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"])),
):
    user_uuid = current_user.uuid
    crud.sales.update_sales(db=db,obj_in=obj_in,user_uuid=user_uuid)
    return {"message": __(key="sales-updated-successfully")}

@router.get("", response_model=None)
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
    return crud.sales.get_many(
        db=db, 
        page=page, 
        per_page=per_page, 
        order=order, 
        order_field=order_field,  # Utilisation du bon nom de variable
        keyword=keyword
    )

@router.get("/total-sales/{sales_date}", response_model=schemas.TotalSalesResponse)
async def total_sales(
    *,
    db: Session = Depends(get_db),
    sales_date: date,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"])),
):
    total_sales = crud.sales.get_total_sales_by_day(db=db, sales_date=sales_date)
    return {"sales_date": sales_date, "total_price": f"{total_sales:,.0f} XAF"}


@router.get("/{uuid}",response_model=schemas.SalesResponseSlim1)
async def read_one(
    *,
    db: Session = Depends(get_db),
    uuid: str,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN","USER"]))
):
    return crud.sales.get_sales_by_uuid(db=db, uuid=uuid)

@router.delete("", response_model=schemas.Msg)
async def delete(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.SalesDelete,
    current_user: models.User = Depends(TokenRequired(roles=["ADMIN"])),
):
    crud.sales.delete(db=db, obj_in=obj_in)
    return {"message": __(key="sales-deleted-successfully")}
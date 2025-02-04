from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime,date

from app.main.schemas.products import ProductSlim
from app.main.schemas.user import UserSlim



class SalesBase(BaseModel):
    product_uuid:str
    customer_uuid:str
    quantity_sales: int
    model_config = ConfigDict(from_attributes=True)


class SalesCreate(SalesBase):
    pass

class SalesUpdate(SalesBase):
    uuid:str
    product_uuid:Optional[str]
    customer_uuid:Optional[str]
    quantity_sales: Optional[int]



class SalesResponseSlim1(BaseModel):
    uuid: str
    quantity_sales: int
    total_price: float
    created_at: datetime
    created_by:UserSlim
    product : ProductSlim

    model_config = ConfigDict(from_attributes=True)


class SalesResponse(BaseModel):
    uuid: str
    quantity_sales: int
    total_price: float
    created_at: datetime
    product : ProductSlim
    created_by:UserSlim
    model_config = ConfigDict(from_attributes=True)

class SalesResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[SalesResponse]

    model_config = ConfigDict(from_attributes=True)


class TotalSalesResponse(BaseModel):
    sales_date: date
    total_price: str
    model_config = ConfigDict(from_attributes=True)


class SalesDelete(BaseModel):
    uuid:str

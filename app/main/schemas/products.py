from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime,date


class ProductBase(BaseModel):
    name: str
    category_uuid:str
    quantity:str
    price: float
    manufacturing_date:date
    expiration_date:date

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    uuid:str
    name: Optional[str]
    category_uuid:Optional[str]
    quantity:Optional[int]
    price:Optional[float]
    manufacturing_date:Optional[date]
    expiration_date:Optional[date]

class ProductDelete(BaseModel):
    uuid:str

class ProductResponse(BaseModel):
    uuid:str
    name: str
    category_uuid:str
    quantity:str
    price: float
    manufacturing_date:date
    expiration_date:date
    created_at:datetime
    updated_at:datetime

class ProductResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[ProductResponse]

    model_config = ConfigDict(from_attributes=True)


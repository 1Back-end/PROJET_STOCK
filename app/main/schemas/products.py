from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime,date

from app.main.schemas.category import CategoryBase
from app.main.schemas.file import FileSlim1
from app.main.schemas.user import UserSlim

class ProductSlim(BaseModel):
    uuid: str
    name: str
    quantity:int
    price: float
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    category_uuid:str
    quantity:int
    price: float
    manufacturing_date:date
    expiration_date:date
    avatar_uuid:Optional[str]

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
    avatar_uuid:Optional[str]

class ProductDelete(BaseModel):
    uuid:str

class ProductResponse(BaseModel):
    uuid:str
    name: str
    category:CategoryBase
    avatar:Optional[FileSlim1]
    quantity:int
    price: float
    manufacturing_date:date
    expiration_date:date
    created_at:datetime
    updated_at:datetime
    created_by:UserSlim

    model_config = ConfigDict(from_attributes=True)


class ProductResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[ProductResponse]

    model_config = ConfigDict(from_attributes=True)


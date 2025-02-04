from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime

from app.main.schemas.user import UserSlim


class CategoryBase(BaseModel):
    name:str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    uuid:str
    name:Optional[str] = None
    description: Optional[str] = None

class CategoryDelete(BaseModel):
    uuid: str

class CategoryResponse(BaseModel):
    uuid: str
    name: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by:UserSlim
    model_config = ConfigDict(from_attributes=True)

class CategoryResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[CategoryResponse]

    model_config = ConfigDict(from_attributes=True)

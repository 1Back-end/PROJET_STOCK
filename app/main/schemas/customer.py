from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime

from app.main.schemas.user import UserSlim


class CustomerBase(BaseModel):
    first_name:str
    last_name:str
    phone_number:str
    email:EmailStr
    address:str

class CustomerCreate(CustomerBase):
    pass

class CustomerDelete(BaseModel):
    uuid:str

class CustomerUpdate(BaseModel):
    uuid:str
    first_name:Optional[str]
    last_name:Optional[str]
    email:Optional[EmailStr]
    phone_number:Optional[str]
    address:Optional[str]

class CustomerResponse(BaseModel):
    uuid:str
    first_name:str
    last_name:str
    phone_number:str
    email:str
    address:Optional[str]
    created_at:datetime
    updated_at:Optional[datetime]
    created_by:UserSlim
    
    model_config = ConfigDict(from_attributes=True)

class CustomerResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[CustomerResponse]

    model_config = ConfigDict(from_attributes=True)
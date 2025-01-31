from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime


class UserBase(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    phone_number:str
    password_hash:str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    uuid:str
    is_active:bool
    created_at:datetime
    updated_at: datetime

class UserProfile(UserBase):
    pass
from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime

from app.main.models.user import UserRole


class UserSlim(BaseModel):
    uuid:str
    first_name:str
    last_name:str
    role:UserRole
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    phone_number:str
    password_hash:str
    role:UserRole

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    firt_name:Optional[str]
    last_name:Optional[str]
    email:Optional[str]
    phone_number:Optional[str]
    avatar_uuid:Optional[str]


class UserResponse(UserBase):
    uuid:str
    is_active:bool
    created_at:datetime
    updated_at: datetime

class UserProfile(UserBase):
    pass


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserAuthentication(BaseModel):
    user: UserBase
    token: Optional[Token] = None
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDetail(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    phone_number:str
    # role:UserRole
    model_config = ConfigDict(from_attributes=True)

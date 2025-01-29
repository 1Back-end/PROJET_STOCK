from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional
from app.main.models.user import UserRole
from datetime import datetime


class UserBase(BaseModel):
    username : str
    email : EmailStr
    phone_number : str
    password_hash:str
    role : UserRole

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    uuid:str
    username:Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    role: Optional[UserRole]

class UserDelete(BaseModel):
    uuid: str

class UserLogin(BaseModel):
    username: str
    password_hash: str

class UserResponse(BaseModel):
    uuid: str
    username: str
    email: EmailStr
    phone_number: str
    role: str
    created_at:datetime

class UserResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[UserResponse]

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserAuthentification(BaseModel):
    admin: UserResponse 
    token: Optional[Token] = None
    model_config = ConfigDict(from_attributes=True)

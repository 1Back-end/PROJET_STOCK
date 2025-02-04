import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.security import get_password_hash,verify_password
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
# from app.main.core.mail import send_mail
from jinja2 import Template
import os


class CRUDUser(CRUDBase[models.User,schemas.UserBase,schemas.UserCreate]):

    @classmethod
    def get_user_by_email(cls,db:Session,*,email:str):
        return db.query(models.User).filter(models.User.email == email,models.User.is_deleted==False).first()
    
    @classmethod
    def authenticate(cls, db: Session, *, email: str, password: str) -> Union[models.User, None]:
        db_obj: models.User = db.query(models.User).filter(models.User.email == email).first()
        if not db_obj:
            return None
        if not verify_password(password, db_obj.password_hash):
            return None
        return db_obj
    
    @classmethod
    def get_user_by_phone_number(cls, db:Session,*, phone_number:str):
        return db.query(models.User).filter(models.User.phone_number == phone_number, models.User.is_deleted==False).first()
    
    @classmethod
    def get_user_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.User).filter(models.User.uuid == uuid, models.User.is_deleted==False).first()    

    @classmethod
    def create_user(cls, db: Session, *, user_in: schemas.UserCreate) -> models.User:
        hashed_password = get_password_hash(user_in.password_hash)
        new_user = models.User(
            uuid=str(uuid.uuid4()),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            phone_number=user_in.phone_number,
            password_hash=hashed_password,
            role = models.UserRole.USER
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @classmethod
    def update_profil(cls, db: Session, *, obj_in: schemas.UserUpdate):
        avatar_uuid=None
        user = cls.get_user_by_uuid(db=db)
    

    
        
user = CRUDUser(models.user)
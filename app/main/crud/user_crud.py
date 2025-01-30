import math
import bcrypt
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

class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):

    @classmethod
    def authenticate(cls, db: Session, *, username: str, password: str) -> Union[models.User, None]:
        db_obj: models.User = db.query(models.User).filter(models.User.username == username).first()
        if not db_obj:
            return None
        if not verify_password(password, db_obj.password_hash):
            return None
        return db_obj
    
    @classmethod
    def get_user_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.User).filter(models.User.uuid == uuid).first()
    
    @classmethod
    def get_by_email(cls,db:Session,email:str):
        return db.query(models.User).filter(models.User.email == email).first()
    
    @classmethod
    def get_by_phone_number(cls, db: Session, phone_number: str):
        return db.query(models.User).filter(models.User.phone_number == phone_number).first()
    
    @classmethod
    def create_user(cls, db: Session, *, obj_in: schemas.UserCreate):
            # Assurez-vous que le mot de passe en clair est utilisé ici
    # Hasher le mot de passe
        hashed_password = get_password_hash(obj_in.password_hash)
        new_user = models.User(
            uuid=str(uuid.uuid4()),  # Génère un UUID unique pour chaque utilisateur
            username=obj_in.username,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            password_hash=hashed_password,
            status=models.UserStatus.ACTIVED,
            role=models.UserRole.ADMIN
        )

        # Ajout de l'utilisateur à la base de données
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    
      
user = CRUDUser(models.User)
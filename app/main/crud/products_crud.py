import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from sqlalchemy.orm import Session
from app.main.core.i18n import __
from app.main.crud.base import CRUDBase
from app.main import models,schemas
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
# from app.main.core.mail import send_mail
from jinja2 import Template
import os


class CRUDProduct(CRUDBase[models.Product,schemas.ProductCreate,schemas.ProductUpdate]):
    
    @classmethod
    def get_product_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Product).filter(models.Product.uuid==uuid,models.Product.is_deleted==False)
    
    @classmethod
    def create_product(cls,db:Session,*,obj_in:schemas.ProductCreate,user_uuid:str):
        new_product = models.Product(
            uuid = str(uuid.uuid4()),
            name=obj_in.name,
            category_uuid=obj_in.category_uuid,
            quantity=obj_in.quantity,
            price = obj_in.price,
            manufacturing_date=obj_in.manufacturing_date,
            expiration_date=obj_in.expiration_date,
            added_by=user_uuid
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    
product = CRUDProduct(models.Product)
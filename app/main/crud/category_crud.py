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


class CRUDCategory(CRUDBase[models.Category,schemas.CategoryCreate,schemas.CategoryUpdate]):

    @classmethod
    def get_category_by_name(cls,db:Session,*,name:str):
        return db.query(models.Category).filter(models.Category.name == name,models.Category.is_deleted==False).first()
    
    @classmethod
    def get_category_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Category).filter(models.Category.uuid == uuid,models.Category.is_deleted==False).first()
    
    @classmethod
    def create_category(cls,db:Session,*,obj_in:schemas.CategoryCreate,user_uuid:str):
        new_category = models.Category(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            description=obj_in.description,
            added_by=user_uuid
        
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    
    @classmethod
    def update_category(cls, db: Session, *, obj_in: schemas.CategoryUpdate,user_uuid:str):
        # Récupérer la catégorie existante
        category = cls.get_category_by_uuid(db,uuid=obj_in.uuid)
        if not category:
            raise HTTPException(status_code=404, detail=__(key="category-not-found."))
        # Mettre à jour les informations
        category.name = obj_in.name if obj_in.name else category.name
        category.description = obj_in.description if obj_in.description else category.description
        db.commit()
        db.refresh(category)
    
    @classmethod
    def delete_category(cls, db: Session, *, obj_in:schemas.CategoryDelete):
        category = cls.get_category_by_uuid(db, uuid=obj_in.uuid)
        if not category:
            raise HTTPException(status_code=404, detail=__(key="category-not-found."))
        category.is_deleted = True
        db.commit()

    @classmethod
    def get_many(
        cls,
        *,
        db: Session,
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = None,
        order_field: Optional[str] = None,
        keyword: Optional[str] = None,  # Paramètre de recherche par mot-clé
    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Category).filter(models.Category.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Category.name.ilike(f'%{keyword}%'),
                    models.Category.description.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Category, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Category, order_field).asc())
            elif order == "desc":
                record_query = record_query.order_by(getattr(models.Category, order_field).desc())

        total = record_query.count()

        # Pagination
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CategoryResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )



category = CRUDCategory(models.Category)
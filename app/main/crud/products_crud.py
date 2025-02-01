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
from app.main import crud, schemas, models
from app.main.crud.storage_crud import get_file_by_uuid
class CRUDProduct(CRUDBase[models.Product,schemas.ProductCreate,schemas.ProductUpdate]):
    
    @classmethod
    def get_product_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Product).filter(models.Product.uuid==uuid,models.Product.is_deleted==False).first()
    @classmethod
    def get_product_by_name(cls,db:Session, *, name:str):
        return db.query(models.Product).filter(models.Product.name==name,models.Product.is_deleted==False).first()
    
    @classmethod
    def create_product(cls,db:Session,*,obj_in:schemas.ProductCreate,user_uuid:str):
        category = crud.category.get_category_by_uuid(db=db,uuid=obj_in.category_uuid)
        if not category:
            raise HTTPException(status_code=404, detail=__(key="category-not-found."))
        avatar = get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found."))
        
        new_product = models.Product(
            uuid = str(uuid.uuid4()),
            name=obj_in.name,
            category_uuid=obj_in.category_uuid,
            quantity=obj_in.quantity,
            price = obj_in.price,
            manufacturing_date=obj_in.manufacturing_date,
            expiration_date=obj_in.expiration_date,
            added_by=user_uuid,
            avatar_uuid=avatar.uuid if avatar else None,
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    
    @classmethod
    def update_product(cls, db: Session, *, obj_in: schemas.ProductUpdate, user_uuid: str):
        # Retrieve the product to be updated by its UUID
        db_obj = cls.get_product_by_uuid(db, uuid=obj_in.uuid)
        if db_obj is None:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        # Verify if the category exists
        category = crud.category.get_category_by_uuid(db=db, uuid=obj_in.category_uuid)
        if not category:
            raise HTTPException(status_code=404, detail=__(key="category-not-found."))
        # Verify if the avatar file exists
        avatar = get_file_by_uuid(db=db, file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found."))
        # Update the fields of the product if the corresponding values exist
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.category_uuid = obj_in.category_uuid if obj_in.category_uuid else db_obj.category_uuid
        db_obj.quantity = obj_in.quantity if obj_in.quantity else db_obj.quantity
        db_obj.price = obj_in.price if obj_in.price else db_obj.price
        db_obj.manufacturing_date = obj_in.manufacturing_date if obj_in.manufacturing_date else db_obj.manufacturing_date
        db_obj.expiration_date = obj_in.expiration_date if obj_in.expiration_date else db_obj.expiration_date
        db_obj.avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else db_obj.avatar_uuid
        
        # Commit the changes to the database
        db.flush()
        db.commit()
        
        # Refresh the instance to reflect the changes
        db.refresh(db_obj)
        
        return db_obj

    @classmethod
    def delete_product(cls,db:Session,*,obj_in:schemas.ProductDelete):
        product = cls.get_product_by_uuid(db,uuid=obj_in.uuid)
        if product is None:
            raise HTTPException(status_code=404,detail=__(key="product-not-found"))
        product.is_deleted=True
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
        record_query = db.query(models.Product).filter(models.Product.is_deleted == False)
        
        # Recherche par mot-clé
        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Product.name.ilike(f"%{keyword}%"),
                    models.Product.category_uuid.ilike(f"%{keyword}%"),
                    models.Product.uuid.ilike(f"%{keyword}%"),
                    models.Product.manufacturing_date.ilike(f"%{keyword}%"),
                    models.Product.expiration_date.ilike(f"%{keyword}%"),
                    models.Product.added_by.ilike(f"%{keyword}%")
                )
            )
        
        # Tri
        if order and order_field and hasattr(models.Product, order_field):
            if order.lower() == "asc":
                record_query = record_query.order_by(getattr(models.Product, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Product, order_field).desc())
        # Pagination
        total = record_query.count()

        # Pagination
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.ProductResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    
product = CRUDProduct(models.Product)
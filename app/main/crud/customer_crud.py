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


class CRUDCustomer(CRUDBase[models.Customer,schemas.CustomerCreate,schemas.CustomerUpdate]):

    @classmethod
    def get_customer_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Customer).filter(models.Customer.uuid==uuid,models.Customer.is_deleted==False).first()
    
    @classmethod
    def get_customer_by_email(cls,db:Session,*,email:str):
        return db.query(models.Customer).filter(models.Customer.email==email,models.Customer.is_deleted==False).first()
    
    @classmethod
    def get_customer_by_phone_number(cls,db:Session,*,phone_number:str):
        return db.query(models.Customer).filter(models.Customer.phone_number==phone_number,models.Customer.is_deleted==False).first()
    
    @classmethod
    def create_customer(cls,db:Session,obj_in:schemas.CustomerCreate,user_uuid:str):
        new_customer = models.Customer(
            uuid=str(uuid.uuid4()),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            address=obj_in.address,
            added_by=user_uuid
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    @classmethod
    def update_customer(cls,db:Session,user_in:schemas.CustomerUpdate,user_uuid:str):
        db_customer = cls.get_customer_by_uuid(db=db,uuid=user_in.uuid)
        if db_customer is None:
            raise HTTPException(status_code=404,detail=__(key="customer-not-found"))
        db_customer.first_name = user_in.first_name if user_in.first_name else db_customer.first_name
        db_customer.last_name = user_in.last_name if user_in.last_name else db_customer.last_name
        db_customer.email = user_in.email if user_in.email else db_customer.email
        db_customer.address = user_in.address if user_in.address else db_customer.address
        db_customer.phone_number = user_in.phone_number if user_in.phone_number else db_customer.phone_number
        db.flush()
        db.commit()
        # Refresh the instance to reflect the changes
        db.refresh(db_customer)
        return db_customer
    
    @classmethod
    def delete_customer(cls,db:Session,*,obj_in:schemas.CustomerDelete):
        obj_user = cls.get_customer_by_uuid(db=db,uuid=obj_in.uuid)
        if obj_user is None:
            raise HTTPException(status_code=404,detail=__(key="customer-not-found"))
        obj_user.is_deleted = True
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

        record_query = db.query(models.Customer).filter(models.Customer.is_deleted==False)
        
        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Customer.first_name.ilike(f'%{keyword}%'),
                    models.Customer.last_name.ilike(f'%{keyword}%'),
                    models.Customer.email.ilike(f'%{keyword}%'),
                    models.Customer.phone_number.ilike(f'%{keyword}%'),
                    models.Customer.address.ilike(f'%{keyword}%'),
                )
            )
        if order and order_field and hasattr(models.Customer, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Customer, order_field).asc())
            elif order == "desc":
                record_query = record_query.order_by(getattr(models.Customer, order_field).desc())

        total = record_query.count()

        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CustomerResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )

        
    
customer = CRUDCustomer(models.Customer)
from datetime import date
import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_,func
import re
from typing import List, Optional, Union
import uuid
from sqlalchemy.orm import Session
from app.main.core.i18n import __
from app.main.crud.base import CRUDBase
from app.main import crud, schemas, models



class CRUDSales(CRUDBase[models.Sale,schemas.SalesBase,schemas.SalesResponse]):

    @classmethod
    def get_sales_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Sale).filter(models.Sale.uuid == uuid, models.Sale.is_deleted == False).first()
    
    @classmethod
    def get_sales_by_customer(cls, db: Session, *, customer_uuid: str):
        customer = crud.customer.get_customer_by_uuid(db=db, uuid=customer_uuid)
        if not customer:
            raise HTTPException(status_code=404, detail=__(key="customer-not-found"))
        sales = db.query(models.Sale).filter(
            models.Sale.customer_uuid == customer_uuid,
            models.Sale.is_deleted == False
        ).all()

        if not sales:
            raise HTTPException(status_code=404, detail=__(key="sales-not-found"))
        return sales

        
    
    @classmethod
    def get_sales_by_product(cls, db: Session,*, product_uuid: str):
        return db.query(models.Sale).filter(models.Sale.product_uuid == product_uuid, models.Sale.is_deleted == False).all()
    

    @classmethod
    def create_sales(cls, db: Session, *,obj_in:schemas.SalesCreate,user_uuid:str):
        product = crud.product.get_product_by_uuid(db=db,uuid=obj_in.product_uuid)

        if not product:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        
        customer = crud.customer.get_customer_by_uuid(db=db, uuid=obj_in.customer_uuid)
        if not customer:
            raise HTTPException(status_code=404, detail=__(key="customer-not-found"))
        
        if product.quantity < obj_in.quantity_sales :
            raise HTTPException(status_code=400, detail=__(key="product-out-of-stock"))
        
        sale = models.Sale(
            uuid=str(uuid.uuid4()),
            product_uuid=obj_in.product_uuid,
            customer_uuid=obj_in.customer_uuid,
            quantity_sales=obj_in.quantity_sales,
            total_price=obj_in.quantity_sales * product.price,
            added_by = user_uuid
        )
        product.quantity -= obj_in.quantity_sales
        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale
    
    @classmethod
    def update_sales(cls, db: Session, *, obj_in: schemas.SalesUpdate, user_uuid: str):
        # Récupérer la vente par UUID
        sale = cls.get_sales_by_uuid(db=db, uuid=obj_in.uuid)
        if not sale:
            raise HTTPException(status_code=404, detail=__(key="sale-not-found"))
        
        # Récupérer le produit par UUID
        product = crud.product.get_product_by_uuid(db=db, uuid=obj_in.product_uuid)
        if not product:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        
        # Récupérer le client par UUID
        customer = crud.customer.get_customer_by_uuid(db=db, uuid=obj_in.customer_uuid)
        if not customer:
            raise HTTPException(status_code=404, detail=__(key="customer-not-found"))
        
        # Remettre dans le stock la quantité vendue précédemment
        product.quantity += sale.quantity_sales
        
        # Réinitialiser la quantité vendue (quantity_sales)
        sale.quantity_sales = 0
        
        # Vérification de la nouvelle quantité demandée
        if product.quantity < obj_in.quantity_sales:
            raise HTTPException(status_code=400, detail=__(key="product-out-of-stock"))
        
        # Mettre à jour la vente avec la nouvelle quantité et recalculer le prix
        sale.product_uuid = obj_in.product_uuid if obj_in.product_uuid else sale.product_uuid
        sale.customer_uuid = obj_in.customer_uuid if obj_in.customer_uuid else sale.customer_uuid
        sale.quantity_sales = obj_in.quantity_sales
        sale.total_price = sale.quantity_sales * product.price
        
        # Réajuster le stock en fonction de la nouvelle quantité
        product.quantity -= sale.quantity_sales
        
        # Sauvegarder les changements dans la base de données
        db.commit()
        db.refresh(sale)
        return sale
    
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
        
        record_query = db.query(models.Sale).filter(models.Sale.is_deleted==False)
        
        if keyword:
            # Recherche par mot-clé
            record_query = record_query.filter(
                or_(
                    models.Sale.uuid.ilike(f"%{keyword}%"),
                    models.Sale.product_uuid.ilike(f"%{keyword}%"),
                    models.Sale.customer_uuid.ilike(f"%{keyword}%"),
                    models.Sale.quantity_sales.ilike(f"%{keyword}%"),
                    models.Sale.total_price.ilike(f"%{keyword}%")
                )
            )
        if order and order_field and hasattr(models.Sale, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Sale, order_field).asc())
            elif order == "desc":
                record_query = record_query.order_by(getattr(models.Sale, order_field).desc())
        total = record_query.count()

        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.SalesResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )


    @classmethod
    def get_total_sales_by_day(cls, db: Session, *, sales_date: date):
        
        total_sales = (
        db.query(func.coalesce(func.sum(models.Sale.total_price), 0))
        .filter(func.date(models.Sale.created_at) == sales_date, models.Sale.is_deleted == False)
        .scalar()
        )
        return total_sales
    
    @classmethod
    def delete_sales(cls,db:Session,*,obj_in:schemas.SalesDelete):
        sale = cls.get_sales_by_uuid(db=db, uuid=obj_in.uuid)
        if not sale:
            raise HTTPException(status_code=404, detail=__(key="sale-not-found"))
        
        sale.is_deleted = True
        db.commit()
        return sale
        

        
    

sales = CRUDSales(models.Sale)
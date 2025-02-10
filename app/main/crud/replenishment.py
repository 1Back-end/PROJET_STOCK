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
from app.main import models,schemas,crud
import os


class CRUDReplenishment(CRUDBase[models.Replenishment,schemas.ReplenishmentCreate,schemas.ReplishmentUpdate]):

    @classmethod
    def create_replenishment(cls,db:Session,*,obj_in:schemas.ReplenishmentCreate,user_uuid:str):
        product =  crud.product.get_product_by_uuid(db=db,uuid=obj_in.product_uuid)
        if not product:
            raise HTTPException(status_code=404,detail=__(key="product-not-found"))
        # replenishment_quantity = product.quantity + obj_in.new_quantity

        new_replenishment = models.Replenishment(
            uuid=str(uuid.uuid4()),
            product_uuid=obj_in.product_uuid,
            new_quantity=obj_in.new_quantity,
            added_by = user_uuid
        )
        db.add(new_replenishment)
        db.commit()
        db.refresh(new_replenishment)
        return new_replenishment
        
        
replenishment = CRUDReplenishment(models.Replenishment)
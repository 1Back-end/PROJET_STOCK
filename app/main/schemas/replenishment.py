from pydantic import BaseModel, ConfigDict,EmailStr
from typing import List, Optional

from datetime import datetime

from app.main.schemas.products import ProductSlim
from app.main.schemas.user import UserSlim


class ReplenishmentBase(BaseModel):
    product_uuid:str
    new_quantity:int

class ReplenishmentCreate(ReplenishmentBase):
    pass

class ReplishmentUpdate(BaseModel):
    product_uuid:Optional[str]=None
    new_quantity:Optional[int]=None

class ResplishmentResponse(BaseModel):
    new_quantity:int
    product:ProductSlim
    created_by:UserSlim
    created_at:datetime
    updated_at:Optional[datetime]

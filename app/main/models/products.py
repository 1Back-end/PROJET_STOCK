from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, event,Boolean,ForeignKey,Float,Date
from app.main.models.db.base_class import Base
from enum import Enum
import uuid
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'products'

    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    category_uuid = Column(String, ForeignKey("categories.uuid"),nullable=False)
    category = relationship("Category", foreign_keys=[category_uuid])
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    manufacturing_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean,default=False)

    added_by = Column(String,ForeignKey("users.uuid"),nullable=False)
    created_by = relationship("User",foreign_keys=[added_by])

    def __repr__(self):
        return f'<Product(uuid="{self.uuid}", name="{self.name}")>'

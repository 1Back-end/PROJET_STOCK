from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, event,Boolean,ForeignKey,Float
from app.main.models.db.base_class import Base
from enum import Enum
import uuid
from sqlalchemy.orm import relationship



class Sale(Base):
    __tablename__ = 'sales'

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

    product_uuid = Column(String,ForeignKey('products.uuid'),nullable=False)
    product = relationship('Product', foreign_keys=[product_uuid])
    customer_uuid = Column(String, ForeignKey('customers.uuid'),nullable=False)
    customer = relationship('Customer', foreign_keys=[customer_uuid])
    added_by = Column(String,ForeignKey("users.uuid"),nullable=True)
    created_by = relationship("User",foreign_keys=[added_by])
    quantity_sales = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'<Sale {self.uuid}>'
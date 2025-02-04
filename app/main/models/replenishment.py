from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, event,Boolean,ForeignKey
from app.main.models.db.base_class import Base
from enum import Enum
import uuid
from sqlalchemy.orm import relationship


class Replenishment(Base):
    __tablename__ = 'replenishment'

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    product_uuid = Column(String,ForeignKey('products.uuid'),nullable=False)
    product = relationship('Product', foreign_keys=[product_uuid])
    new_quantity = Column(Integer,nullable=False)
    added_by = Column(String,ForeignKey("users.uuid"),nullable=False)
    created_by = relationship("User",foreign_keys=[added_by])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Replenishment {self.uuid}>"

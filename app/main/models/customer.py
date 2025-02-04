from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, event,Boolean,ForeignKey
from app.main.models.db.base_class import Base
from enum import Enum
import uuid
from sqlalchemy.orm import relationship


class Customer(Base):
    __tablename__ = 'customers'

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    phone_number = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False, unique=True)
    address = Column(String,nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    added_by = Column(String,ForeignKey("users.uuid"),nullable=True)
    created_by = relationship("User",foreign_keys=[added_by])
    
    def __repr__(self):
        return f'<Customer {self.uuid}>'
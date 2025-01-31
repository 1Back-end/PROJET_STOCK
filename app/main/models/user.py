from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, event,Boolean
from app.main.models.db.base_class import Base
from enum import Enum
import uuid



class User(Base):
    __tablename__ = 'users'
    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f'<User {self.uuid}>'
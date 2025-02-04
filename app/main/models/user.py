from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, event,Boolean,ForeignKey
from app.main.models.db.base_class import Base
from enum import Enum
import uuid
from sqlalchemy.orm import relationship
class UserRole(str, Enum):
    ADMIN = "ADMIN",
    USER = "USER"



class User(Base):
    __tablename__ = 'users'
    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    role = Column(String, default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reset_password_code = Column(String, nullable=True)
    reset_code_sent_at = Column(DateTime, nullable=True)
    avatar_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    avatar = relationship("Storage", foreign_keys=[avatar_uuid])

    


    def __repr__(self):
        return f'<User {self.uuid}>'
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, event
from app.main.models.db.base_class import Base
from enum import Enum
import uuid

class AuthStatus(str,Enum):
    ACTIVED = "ACTIVED"
    DELETED = "DELETED"
    UNACTIVED = "UNACTIVED"
    BLOCKED = "BLOCKED"

class Authrole(str,Enum):
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class Auth(Base):
    __tablename__ = "auth"

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String,index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    status = Column(String, default=AuthStatus.ACTIVED)
    role = Column(String, default=Authrole.ADMIN)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(uuid='{self.uuid}', username='{self.username}', email='{self.email}', phone_number='{self.phone_number}', status='{self.status}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"
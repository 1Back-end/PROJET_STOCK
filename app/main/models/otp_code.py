from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from app.main.models.db.base_class import Base
from datetime import datetime, timedelta
import uuid


class OTPCode(Base):
    __tablename__ = "otp_codes"

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False)
    otp_code = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)

    def is_valid(self):
        return not self.is_used and self.expires_at > datetime.utcnow()
    
    def __repr__(self):
        return f'<OTPCode {self.uuid}>'

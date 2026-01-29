from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class FormData(Base):
    """Model for storing form data associated with UUIDs"""
    __tablename__ = "form_data"
    
    uuid = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    company = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<FormData(uuid={self.uuid}, name={self.name})>"

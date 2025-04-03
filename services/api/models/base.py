from sqlalchemy import Column, DateTime, Integer
from datetime import datetime
from ..core.database import Base

class BaseModel(Base):
    """Base model class that includes common fields"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
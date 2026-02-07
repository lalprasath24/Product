from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from app.models.document import Base

class DatabaseConfig(Base):
    __tablename__ = "database_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    db_type = Column(String(50), nullable=False)  # mysql, postgresql, sqlite
    host = Column(String(255))
    port = Column(Integer)
    database = Column(String(255), nullable=False)
    username = Column(String(255))
    password = Column(String(255))
    schema_info = Column(Text)  # JSON string of schema
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSVECTOR

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384))
    content_tsv = Column(TSVECTOR)  # Full-text search vector
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('documents_content_tsv_idx', 'content_tsv', postgresql_using='gin'),
    )
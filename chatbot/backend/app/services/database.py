import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from app.models.document import Base, Document
from app.models.database_config import DatabaseConfig
from app.core.config import settings

logger = logging.getLogger("remo_ai")

DATABASE_URL = settings.DATABASE_URL
EMBEDDING_MODEL = settings.EMBEDDING_MODEL

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

async def init_db():
    """Initialize database and create tables"""
    try:
        logger.info("Initializing database...")
        # Create extension and tables
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

async def store_document(filename: str, content: str):
    """Store document with its vector embedding"""
    db = SessionLocal()
    
    try:
        logger.info(f"Storing document: {filename}")
        # Generate embedding
        embedding = embedding_model.encode(content)
        
        # Store in database
        doc = Document(
            filename=filename,
            content=content,
            embedding=embedding.tolist()
        )
        
        db.add(doc)
        db.commit()
        logger.info(f"Document stored successfully: {filename}")
    except Exception as e:
        logger.error(f"Failed to store document {filename}: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

async def search_documents(query: str, limit: int = 3) -> List[Tuple[str, float]]:
    """Search for similar documents using vector similarity"""
    db = SessionLocal()
    
    try:
        logger.info(f"Searching documents for query: {query[:50]}...")
        # Generate query embedding
        query_embedding = embedding_model.encode(query)
        
        # Search for similar documents using cosine similarity
        sql = text("""
            SELECT content, 1 - (embedding <=> CAST(:embedding AS vector)) as similarity
            FROM documents
            WHERE 1 - (embedding <=> CAST(:embedding AS vector)) > 0.3
            ORDER BY similarity DESC
            LIMIT :limit
        """)
        
        results = db.execute(sql, {
            "embedding": str(query_embedding.tolist()),
            "limit": limit
        }).fetchall()
        
        logger.info(f"Found {len(results)} similar documents")
        return [(row[0], row[1]) for row in results]
        
    except Exception as e:
        logger.error(f"Document search failed: {str(e)}")
        raise
    finally:
        db.close()

async def get_all_documents():
    """Get all documents from database"""
    db = SessionLocal()
    try:
        logger.info("Retrieving all documents")
        documents = db.query(Document).all()
        logger.info(f"Retrieved {len(documents)} documents")
        return documents
    except Exception as e:
        logger.error(f"Failed to retrieve documents: {str(e)}")
        raise
    finally:
        db.close()

async def delete_document(filename: str):
    """Delete document by filename"""
    db = SessionLocal()
    try:
        logger.info(f"Deleting document: {filename}")
        deleted_count = db.query(Document).filter(Document.filename == filename).delete()
        db.commit()
        
        if deleted_count > 0:
            logger.info(f"Document deleted successfully: {filename}")
        else:
            logger.warning(f"Document not found: {filename}")
            
    except Exception as e:
        logger.error(f"Failed to delete document {filename}: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
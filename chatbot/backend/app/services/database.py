import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from app.models.document import Base, Document
from app.models.database_config import DatabaseConfig
from app.core.config import settings
from app.services.search_utils import hybrid_rrf_search

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
        
        # Create HNSW index for vector similarity
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS documents_embedding_hnsw_idx
                ON documents
                USING hnsw (embedding vector_cosine_ops)
            """))
            
            # Create trigger to auto-update full-text search vector
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION documents_tsv_trigger() RETURNS trigger AS $$
                BEGIN
                    NEW.content_tsv := to_tsvector('english', NEW.content);
                    RETURN NEW;
                END
                $$ LANGUAGE plpgsql
            """))
            
            conn.execute(text("""
                DROP TRIGGER IF EXISTS documents_tsv_update ON documents
            """))
            
            conn.execute(text("""
                CREATE TRIGGER documents_tsv_update
                BEFORE INSERT OR UPDATE ON documents
                FOR EACH ROW EXECUTE FUNCTION documents_tsv_trigger()
            """))
            
            conn.commit()
        
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
    """Hybrid search: Vector similarity + Full-text search with RRF"""
    db = SessionLocal()
    
    try:
        logger.info(f"Hybrid search for query: {query[:50]}...")
        query_embedding = embedding_model.encode(query).tolist()
        
        results = hybrid_rrf_search(db, query_embedding, query, limit)
        
        logger.info(f"Found {len(results)} documents via hybrid search")
        return results
        
    except Exception as e:
        logger.error(f"Hybrid search failed: {str(e)}")
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
"""
Migration script to add hybrid search support to existing database
Run this once: python migrate_add_hybrid_search.py
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Add content_tsv column
            logger.info("Adding content_tsv column...")
            conn.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS content_tsv TSVECTOR"))
            
            # Create GIN index
            logger.info("Creating GIN index...")
            conn.execute(text("CREATE INDEX IF NOT EXISTS documents_content_tsv_idx ON documents USING gin(content_tsv)"))
            
            # Create trigger function
            logger.info("Creating trigger function...")
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION documents_tsv_trigger() RETURNS trigger AS $$
                BEGIN
                    NEW.content_tsv := to_tsvector('english', NEW.content);
                    RETURN NEW;
                END
                $$ LANGUAGE plpgsql
            """))
            
            # Create trigger
            logger.info("Creating trigger...")
            conn.execute(text("DROP TRIGGER IF EXISTS documents_tsv_update ON documents"))
            conn.execute(text("""
                CREATE TRIGGER documents_tsv_update
                BEFORE INSERT OR UPDATE ON documents
                FOR EACH ROW EXECUTE FUNCTION documents_tsv_trigger()
            """))
            
            # Populate existing data
            logger.info("Populating content_tsv for existing documents...")
            result = conn.execute(text("UPDATE documents SET content_tsv = to_tsvector('english', content)"))
            logger.info(f"Updated {result.rowcount} documents")
            
            conn.commit()
            logger.info("✅ Migration completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    migrate()

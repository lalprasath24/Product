from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import logging
import json
from typing import Optional
from app.services.database import get_all_documents, delete_document
from app.services.langchain_service import rag_service
from app.services.redis_service import redis_service
from app.services.text_to_sql_service import text_to_sql_service

logger = logging.getLogger("remo_ai")
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    chat_type: Optional[str] = "rag"  # "rag" or "sql"

class ChatResponse(BaseModel):
    response: str

class DatabaseConfigRequest(BaseModel):
    name: str
    db_type: str
    host: str
    port: int
    database: str
    username: str
    password: str

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"File upload request: {file.filename}")
    
    try:
        if not file.filename.endswith('.txt'):
            logger.warning(f"Invalid file type uploaded: {file.filename}")
            raise HTTPException(status_code=400, detail="Only .txt files allowed")
        
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Store in both database and vector store
        from app.services.database import store_document
        await store_document(file.filename, text_content)
        await rag_service.add_document(file.filename, text_content)
        
        logger.info(f"File uploaded successfully: {file.filename}")
        return {"success": True, "filename": file.filename}
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail="File upload failed")

@router.get("/files")
async def get_files():
    logger.info("Files list request")
    
    try:
        documents = await get_all_documents()
        files_list = [{
            "name": doc.filename, 
            "uploadDate": doc.created_at.strftime("%Y-%m-%d") if doc.created_at else "Unknown"
        } for doc in documents]
        
        logger.info(f"Retrieved {len(files_list)} files")
        return files_list
        
    except Exception as e:
        logger.error(f"Failed to retrieve files: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve files")

@router.delete("/files/{filename}")
async def delete_file(filename: str):
    logger.info(f"File deletion request: {filename}")
    
    try:
        await delete_document(filename)
        await rag_service.delete_document(filename)
        logger.info(f"File deleted successfully: {filename}")
        return {"success": True}
        
    except Exception as e:
        logger.error(f"File deletion failed: {str(e)}")
        raise HTTPException(status_code=500, detail="File deletion failed")

@router.get("/test")
async def test_endpoint():
    logger.info("Test endpoint accessed")
    return {"message": "Backend is working!"}

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    logger.info(f"History request for session: {session_id}")
    try:
        history = redis_service.get_chat_history(session_id)
        return {"history": history}
    except Exception as e:
        logger.error(f"Failed to retrieve history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history")

@router.post("/database/config")
async def configure_database(config: DatabaseConfigRequest):
    logger.info(f"Database config request: {config.name}")
    try:
        from app.services.database import SessionLocal
        from app.models.database_config import DatabaseConfig
        
        db = SessionLocal()
        
        # Test connection and analyze schema
        config_dict = config.dict()
        schema = text_to_sql_service.analyze_schema(config_dict)
        
        # Store configuration
        db_config = DatabaseConfig(
            name=config.name,
            db_type=config.db_type,
            host=config.host,
            port=config.port,
            database=config.database,
            username=config.username,
            password=config.password,
            schema_info=json.dumps(schema)
        )
        
        db.add(db_config)
        db.commit()
        db.close()
        
        return {"success": True, "message": "Database configured successfully", "tables": list(schema.keys())}
        
    except Exception as e:
        logger.error(f"Database config failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database configuration failed: {str(e)}")

@router.get("/database/configs")
async def get_database_configs():
    try:
        from app.services.database import SessionLocal
        from app.models.database_config import DatabaseConfig
        
        db = SessionLocal()
        configs = db.query(DatabaseConfig).filter(DatabaseConfig.is_active == True).all()
        db.close()
        
        return [{"id": c.id, "name": c.name, "db_type": c.db_type, "database": c.database} for c in configs]
        
    except Exception as e:
        logger.error(f"Get configs failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get database configs")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Chat request received: {request.message[:50]}... Type: {request.chat_type}")
    
    try:
        if request.chat_type == "sql":
            # Handle SQL chat
            from app.services.database import SessionLocal
            from app.models.database_config import DatabaseConfig
            
            db = SessionLocal()
            db_config = db.query(DatabaseConfig).filter(DatabaseConfig.is_active == True).first()
            db.close()
            
            if not db_config:
                return ChatResponse(response="No database configured. Please configure a database first.")
            
            # Convert to dict and parse schema
            config_dict = {
                "db_type": db_config.db_type,
                "host": db_config.host,
                "port": db_config.port,
                "database": db_config.database,
                "username": db_config.username,
                "password": db_config.password
            }
            schema = json.loads(db_config.schema_info)
            
            # Generate SQL
            sql_query = text_to_sql_service.generate_sql(request.message, schema)
            
            if sql_query == "I need more information.":
                response = "I need more information to answer your question."
            else:
                # Execute query
                try:
                    results = text_to_sql_service.execute_query(sql_query, config_dict)
                    response = text_to_sql_service.summarize_results(request.message, sql_query, results)
                except Exception as e:
                    response = f"Query execution failed: {str(e)}"
        else:
            # Handle RAG chat
            response = await rag_service.search_and_answer(request.message)
        
        # Save to Redis for chat history display only
        redis_service.add_message(request.session_id, "user", request.message)
        redis_service.add_message(request.session_id, "assistant", response)
        
        logger.info("Response generated successfully")
        return ChatResponse(response=response)
        
    except Exception as e:
        logger.error(f"Chat request failed: {str(e)}")
        return ChatResponse(response="I'm having trouble processing your request. Please try again.")
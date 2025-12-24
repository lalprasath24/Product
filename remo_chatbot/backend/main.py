# main.py
from fastapi import FastAPI, HTTPException,Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from schemas import ChatRequest, DBConfig, app_state,Item
from db_manager import get_database_schema, execute_sql_query
from llm_agent import generate_sql_query, interpret_sql_results
from typing import Optional
import sqlite3

app = FastAPI(title="Remo Chatbot Agent")

# ... CORS Middleware ...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ok"}

# @app.post("/items")
# def create_item(item:Item):
#     return {f"name:{item.name},age:{item.age}"}

# @app.post('/requery_param/{age}')
# def requery_param(age:int,name:Optional[str],header:Optional[str]=Header(None)):
#     return {f'age:{ age},name:{name},header:{header}'}      

@app.post("/configure-db")
def configure_database(config: DBConfig):
    """
    Endpoint to receive and store the user's database credentials.
    """
    try:
        # Test the connection by fetching schema
        test_schema = get_database_schema(config) 
        if "Error" in test_schema:
            raise Exception(test_schema)
        
    #     con=sqlite3.connect(f"{config.dbname}")
    #     cursor =con.cursor()
    #     cursor.execute("CREATE TABLE db_details(db_type,host,port,user,password,dbname)")
    #     cursor.execute(f"""
    #     INSERT INTO db_details VALUES
    #         ('{config.db_type}','{config.host}',{config.port},'{config.user}','{config.password}','{config.dbname}')
            
    # """)
            
        app_state.db_config = config
        return {"message": f"Database configuration successful for {config.db_type.value}."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database connection failed: {e}")

@app.get("/get_db")
def get_db_details():
    pass


@app.post("/chat")
def chat_with_db(request: ChatRequest):
    """
    Enhanced chat endpoint with improved error handling and validation.
    """
    if not app_state.db_config:
        raise HTTPException(status_code=400, detail="Database is not configured. Please configure database first.")

    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        config = app_state.db_config
    
        # Get Database Schema
        schema = get_database_schema(config)
        if "Error" in schema:
            raise HTTPException(status_code=500, detail=f"Failed to get schema: {schema}")

        # Generate SQL Query with enhanced prompting
        sql_query = generate_sql_query(request.question, schema, config.db_type.value)
        if "Error" in sql_query:
            raise HTTPException(status_code=500, detail=f"Failed to generate SQL: {sql_query}")

        # Execute SQL Query
        results = execute_sql_query(config, sql_query)
        
        # Interpret Results with context
        final_answer = interpret_sql_results(request.question, sql_query, results)
        
        return {
            "answer": final_answer, 
            "sql_query": sql_query,
            "row_count": len(results.get('rows', [])) if 'rows' in results else 0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
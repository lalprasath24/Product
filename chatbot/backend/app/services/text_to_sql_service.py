import json
import logging
import sqlalchemy
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import create_engine, text, inspect
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from app.core.config import settings

logger = logging.getLogger("remo_ai")

class TextToSQLService:
    def __init__(self):
        self.openrouter_llm = ChatOpenAI(
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            model_name="openai/gpt-3.5-turbo",
            temperature=0
        )
        
        # Ollama for summarization (assuming local setup)
        try:
            from langchain_community.llms import Ollama
            self.ollama_llm = Ollama(model="llama2", base_url="http://localhost:11434")
        except:
            self.ollama_llm = self.openrouter_llm  # Fallback to OpenRouter
    
    def build_connection_string(self, config: Dict) -> str:
        """Build database connection string"""
        if config["db_type"] == "postgresql":
            return f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        elif config["db_type"] == "mysql":
            return f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        elif config["db_type"] == "sqlite":
            return f"sqlite:///{config['database']}"
        else:
            raise ValueError(f"Unsupported database type: {config['db_type']}")
    
    def analyze_schema(self, config: Dict) -> Dict:
        """Analyze database schema and return table/column info"""
        try:
            conn_str = self.build_connection_string(config)
            engine = create_engine(conn_str)
            inspector = inspect(engine)
            
            schema = {}
            for table_name in inspector.get_table_names():
                columns = []
                for column in inspector.get_columns(table_name):
                    columns.append({
                        "name": column["name"],
                        "type": str(column["type"]),
                        "nullable": column["nullable"]
                    })
                schema[table_name] = columns
            
            engine.dispose()
            return schema
            
        except Exception as e:
            logger.error(f"Schema analysis failed: {str(e)}")
            raise
    
    def generate_sql(self, question: str, schema: Dict) -> str:
        """Convert natural language to SQL using OpenRouter"""
        schema_text = self._format_schema_for_prompt(schema)
        
        prompt = f"""You are a SQL expert. Convert the following question to a SELECT query.

Database Schema:
{schema_text}

Rules:
- Generate ONLY SELECT queries
- Use proper table and column names from the schema
- If unclear, respond with "I need more information."

Question: {question}

SQL Query:"""

        try:
            response = self.openrouter_llm.invoke(prompt)
            sql_query = response.content.strip()
            
            if "I need more information" in sql_query:
                return "I need more information."
            
            # Basic validation - ensure it's a SELECT query
            if not sql_query.upper().strip().startswith("SELECT"):
                return "I need more information."
                
            return sql_query
            
        except Exception as e:
            logger.error(f"SQL generation failed: {str(e)}")
            return "I need more information."
    
    def execute_query(self, sql: str, config: Dict) -> List[Dict]:
        """Execute SQL query and return results"""
        try:
            conn_str = self.build_connection_string(config)
            engine = create_engine(conn_str)
            
            with engine.connect() as conn:
                result = conn.execute(text(sql))
                columns = result.keys()
                rows = result.fetchall()
                
                # Convert to list of dictionaries with date serialization
                data = []
                for row in rows:
                    row_dict = {}
                    for col, val in zip(columns, row):
                        if isinstance(val, (date, datetime)):
                            row_dict[col] = val.isoformat()
                        elif isinstance(val, Decimal):
                            row_dict[col] = float(val)
                        else:
                            row_dict[col] = val
                    data.append(row_dict)
                
            engine.dispose()
            return data
            
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def summarize_results(self, question: str, sql: str, results: List[Dict]) -> str:
        """Convert query results to natural language using Ollama"""
        if not results:
            return "No data found for your question."
        
        # Limit results for summarization
        sample_results = results[:5] if len(results) > 5 else results
        
        prompt = f"""Summarize the following database query results in natural language.

Original Question: {question}
SQL Query: {sql}
Results: {json.dumps(sample_results, indent=2)}
Total Records: {len(results)}

Provide a clear, concise summary:"""

        try:
            response = self.ollama_llm.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            # Fallback to simple summary
            return f"Found {len(results)} records. Sample data: {json.dumps(sample_results[:2], indent=2)}"
    
    def _format_schema_for_prompt(self, schema: Dict) -> str:
        """Format schema for LLM prompt"""
        schema_text = ""
        for table, columns in schema.items():
            schema_text += f"\nTable: {table}\n"
            for col in columns:
                schema_text += f"  - {col['name']} ({col['type']})\n"
        return schema_text

text_to_sql_service = TextToSQLService()
# llm_agent.py (OpenRouter Integration)
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

# Using GPT-4 for better SQL generation accuracy
SQL_MODEL = "openai/gpt-4o-mini"
# Using a faster model for interpretation
INTERPRET_MODEL = "openai/gpt-3.5-turbo"


def generate_sql_query(question: str, schema_info: str, db_type: str) -> str:
    """
    Uses the LLM to convert a natural language question into a SQL query
    for the specified database type with enhanced accuracy.
    """
    
    dialect_name = "PostgreSQL" if db_type == 'postgres' else "MySQL" if db_type == 'mysql' else "SQL"
    
    system_prompt = f"""You are an expert {dialect_name} database assistant specialized in generating accurate SQL queries.
Rules:
1. Generate ONLY valid {dialect_name} syntax
2. Use proper table and column names from the schema
3. Handle aggregations, joins, and filters correctly
4. Return ONLY the SQL query without explanations or markdown
5. Use appropriate LIMIT clauses for large result sets"""

    user_prompt = f"""Database Schema:
{schema_info}

User Question: {question}

Generate a precise {dialect_name} query to answer this question. Output only the SQL query."""
    
    try:
        response = client.chat.completions.create(
            model=SQL_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=500
        )
        sql_query = response.choices[0].message.content.strip()
        
        # Clean markdown formatting
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        elif sql_query.startswith("```"):
            sql_query = sql_query[3:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
            
        return sql_query.strip()
        
    except Exception as e:
        print(f"Error calling OpenRouter (Text-to-SQL): {e}")
        return f"Error: Could not generate SQL. {e}"


def interpret_sql_results(question: str, sql_query: str, results: dict) -> str:
    """
    Interprets SQL results and provides a natural language answer with enhanced context.
    """
    if "error" in results:
        return f"I encountered an error while querying the database: {results['error']}"
    
    columns = results.get('columns', [])
    rows = results.get('rows', [])
    
    if not rows:
        return f"I found no results for your question: '{question}'. The database query returned empty."
    
    # Format results for better readability
    results_str = f"Columns: {', '.join(columns)}\n"
    results_str += f"Number of rows: {len(rows)}\n"
    if len(rows) <= 10:
        results_str += "Data:\n"
        for row in rows:
            results_str += f"  {row}\n"
    else:
        results_str += f"First 10 rows:\n"
        for row in rows[:10]:
            results_str += f"  {row}\n"
        results_str += f"... and {len(rows) - 10} more rows"
    
    system_prompt = """You are a helpful data assistant that provides clear, concise answers.
Rules:
1. Answer the user's question directly based on the data
2. Use natural language and avoid technical jargon
3. Format numbers and data clearly
4. If there are multiple results, summarize appropriately
5. Be conversational and helpful"""
    
    user_prompt = f"""User Question: {question}

SQL Query Executed: {sql_query}

Query Results:
{results_str}

Provide a clear, natural language answer to the user's question based on these results."""
    
    try:
        response = client.chat.completions.create(
            model=INTERPRET_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error calling OpenRouter (SQL-to-Text): {e}")
        return f"Error: Could not interpret results. {e}"

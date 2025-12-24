# db_manager.py
import psycopg2
import mysql.connector
from psycopg2.extensions import connection as PgConnection
from mysql.connector.connection import MySQLConnection
from schemas import DBConfig, DBType
from contextlib import contextmanager

# Unified type hint for a connection
DbTypeConnection = PgConnection | MySQLConnection

@contextmanager
def get_db_connection(config: DBConfig) -> DbTypeConnection:
    """
    Provides a database connection based on the db_type.
    """
    conn = None
    try:
        if config.db_type == DBType.postgres:
            conn = psycopg2.connect(
                dbname=config.dbname,
                user=config.user,
                password=config.password,
                host=config.host,
                port=config.port
            )
        elif config.db_type == DBType.mysql:
            conn = mysql.connector.connect(
                database=config.dbname,
                user=config.user,
                password=config.password,
                host=config.host,
                port=config.port
            )
        else:
            raise ValueError(f"Unsupported db_type: {config.db_type}")
        
        yield conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def _get_postgres_schema(conn: PgConnection) -> str:
    """Fetches schema for PostgreSQL."""
    schema_info = ""
    query = """
    SELECT t.table_name, c.column_name, c.data_type 
    FROM information_schema.tables AS t
    JOIN information_schema.columns AS c 
        ON t.table_name = c.table_name
    WHERE t.table_schema = 'public'
    ORDER BY t.table_name, c.ordinal_position;
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        current_table = ""
        for table, column, data_type in rows:
            if table != current_table:
                schema_info += f"\nTable: {table}\n"
                current_table = table
            schema_info += f"  - {column} ({data_type})\n"
    return schema_info

def _get_mysql_schema(conn: MySQLConnection, dbname: str) -> str:
    """Fetches schema for MySQL."""
    schema_info = ""
    query = f"""
    SELECT t.table_name, c.column_name, c.data_type 
    FROM information_schema.tables AS t
    JOIN information_schema.columns AS c 
        ON t.table_name = c.table_name
    WHERE t.table_schema = '{dbname}'
    ORDER BY t.table_name, c.ordinal_position;
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        current_table = ""
        for table, column, data_type in rows:
            if table != current_table:
                schema_info += f"\nTable: {table}\n"
                current_table = table
            schema_info += f"  - {column} ({data_type})\n"
    return schema_info

def get_database_schema(config: DBConfig) -> str:
    """
    Fetches the schema based on the configured db_type.
    """
    try:
        with get_db_connection(config) as conn:
            if config.db_type == DBType.postgres:
                return _get_postgres_schema(conn)
            elif config.db_type == DBType.mysql:
                return _get_mysql_schema(conn, config.dbname)
    except Exception as e:
        return f"Error fetching schema: {e}"

def execute_sql_query(config: DBConfig, sql_query: str) -> dict:
    """
    Executes a given SQL query on the database.
    WARNING: This is a major security risk. See security section.
    """
    
    # 🚨 SECURITY GUARD: Only allow SELECT statements
    if not sql_query.strip().upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed."}

    try:
        with get_db_connection(config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                
                # Check if query produced results (like SELECT)
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    results = cursor.fetchall()
                    return {"columns": columns, "rows": results}
                else:
                    return {"message": "Query executed successfully."}
    except Exception as e:
        # Handle different error types if needed
        return {"error": str(e)}
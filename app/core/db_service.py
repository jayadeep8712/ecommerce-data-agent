import sqlite3
import pandas as pd
import os # <-- Import os

# --- KEY CHANGE: Make the DB path absolute ---
# This finds the directory of the current file (db_service.py)
# then goes up two levels to the project root, and then finds the db file.
# ProjectRoot/app/core/db_service.py -> ProjectRoot/ecommerce_data.db
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(_project_root, 'ecommerce_data.db')


def get_db_schema():
    """Gets the schema of all tables in the database."""
    # Check if the database file exists before trying to connect
    if not os.path.exists(DB_PATH):
        return "Error: Database file not found at " + DB_PATH

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    schema_info = ""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        schema_info += f"Table '{table_name}':\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            schema_info += f"  - {col[1]} ({col[2]})\n"
        schema_info += "\n"
        
    conn.close()
    return schema_info

def execute_query(query: str):
    """Executes a SQL query and returns the result as a pandas DataFrame."""
    try:
        if not os.path.exists(DB_PATH):
            return None, "Database file not found at " + DB_PATH
            
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)
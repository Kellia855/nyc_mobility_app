"""
Script to initialize the MySQL database for NYC Mobility App
"""
import sys
import os
import mysql.connector
from mysql.connector import Error

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import get_db_config

def create_database():
    """Create the database if it doesn't exist"""
    # Connect to MySQL server without specifying a database
    try:
        config = get_db_config()
        conn = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"]
        )
        
        if not conn.is_connected():
            print("Failed to connect to MySQL server")
            return False
            
        cursor = conn.cursor()
        
        # Read the init_db.sql file
        init_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                   "database", "init_db.sql")
        
        with open(init_db_path, 'r') as sql_file:
            # Split the SQL file into statements
            sql_statements = sql_file.read().split(';')
            
            # Execute each statement
            for statement in sql_statements:
                if statement.strip():
                    cursor.execute(statement)
                    
        print("Database created successfully!")
        
        # Now connect to the created database and create tables
        conn.database = "nyc_mobility"
        
        # Read the schema.sql file
        schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  "models", "schema.sql")
        
        with open(schema_path, 'r') as schema_file:
            # Split the schema file into statements
            schema_statements = schema_file.read().split(';')
            
            # Execute each statement
            for statement in schema_statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        print(f"Error executing schema statement: {e}")
        
        print("Tables created successfully!")
        return True
        
    except Error as e:
        print(f"Error: {e}")
        return False
        
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    success = create_database()
    if success:
        print("Database initialization completed successfully!")
    else:
        print("Database initialization failed!")

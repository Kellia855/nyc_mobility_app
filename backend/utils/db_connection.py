"""
Database connection utilities for the NYC Mobility App
"""
import mysql.connector
from mysql.connector import Error
from ..config.db_config import get_db_config

def create_connection():
    """Create a connection to the MySQL database"""
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
        return None
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(conn, query, params=None, fetch=True):
    """Execute a query and return results if applicable"""
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            return cursor.fetchall()
        
        conn.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()

def close_connection(conn):
    """Close the database connection"""
    if conn and conn.is_connected():
        conn.close()

"""
Database configuration settings for NYC Mobility App

IMPORTANT:
- Modify these values with your own MySQL credentials
- Do not commit this file to GitHub with your actual passwords
- This file should be in .gitignore
"""

# Database configuration - MODIFY THESE VALUES
MYSQL_HOST = "localhost"
MYSQL_USER = "kellia"       # Change to your MySQL username
MYSQL_PASSWORD = "pass123"  # Change to your MySQL password
MYSQL_DB = "nyc_mobility"   # (keep this the same)

def get_db_config():
    """Returns database configuration dictionary"""
    return {
        "host": MYSQL_HOST,
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "database": MYSQL_DB
    }

# Database configuration settings
MYSQL_HOST = "localhost"
MYSQL_USER = "kellia"
MYSQL_PASSWORD = "pass123"
MYSQL_DB = "nyc_mobility"

def get_db_config():
    """Returns database configuration dictionary"""
    return {
        "host": MYSQL_HOST,
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "database": MYSQL_DB
    }

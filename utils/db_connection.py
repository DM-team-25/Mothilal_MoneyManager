import mysql.connector
from config.db_config import db_config

def get_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as exceptionhandel:
        print(f"Database connection error: {exceptionhandel}")
        return None

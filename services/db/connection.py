# db/connection.py
import psycopg
import os
from contextlib import contextmanager

# Load environment variables for database configuration (optional, but recommended)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'mydatabase')
DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')

def get_connection():
    """Establish the connection pool or client for PostgreSQL"""
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@contextmanager
def get_cursor():
    """Context manager to handle connection opening and closing"""
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
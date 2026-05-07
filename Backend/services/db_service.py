# services/db_service.py
import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

def get_connection():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    
    if not all([host, port, dbname, user, password]):
        missing = []
        if not host: missing.append("DB_HOST")
        if not port: missing.append("DB_PORT")
        if not dbname: missing.append("DB_NAME")
        if not user: missing.append("DB_USER")
        if not password: missing.append("DB_PASSWORD")
        
        error_msg = f"Missing database environment variables: {', '.join(missing)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error("Database connection failed: %s", e)
        raise

def execute_query(query, params=None, fetch_result=False):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)

        result = None
        if fetch_result:
            result = cursor.fetchone()

        conn.commit()
        return result if fetch_result else cursor.rowcount
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_one(query, params=None):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(query, params)
        result = cur.fetchone()

        cur.close()
        conn.close()

        return result
    except Exception as e:
        logger.exception("fetch_one error: %s", e)
        raise

def fetch_all(query, params=None):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(query, params or ())
        result = cur.fetchall()

        cur.close()
        conn.close()

        return result

    except Exception as e:
        logger.exception("fetch_all error: %s", e)
        return []
    
    
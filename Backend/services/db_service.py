# services/db_service.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

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
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(query, params)
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

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
        print("DB Fetch All Error:", e)
        return []
    
    
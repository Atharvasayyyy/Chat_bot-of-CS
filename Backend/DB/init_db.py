import psycopg2
import os

def get_connection():
    # Hardcoded credentials (temporary fix for connection issues)
    return psycopg2.connect(
        host="database-1.chyse2msct9e.ap-south-1.rds.amazonaws.com",
        port="5432",
        dbname="postgres",
        user="postgres",
        password="AtharvaSable",
        connect_timeout=30,  # Increased timeout
        keepalives=1,
        keepalives_idle=5,
        keepalives_interval=2,
        keepalives_count=2
    )
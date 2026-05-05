# db/seed_users.py

from init_db import get_connection
import random

def seed_users():
    conn = get_connection()
    cur = conn.cursor()

    for i in range(1, 51):
        user_id = f"U{i:03}"
        name = f"User{i}"
        email = f"user{i}@gmail.com"
        complaints = random.randint(0, 3)

        cur.execute("""
        INSERT INTO users (user_id, name, email, complaint_count)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING
        """, (user_id, name, email, complaints))

    conn.commit()
    cur.close()
    conn.close()

seed_users()
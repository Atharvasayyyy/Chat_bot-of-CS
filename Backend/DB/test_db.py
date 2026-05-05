# db/test_db.py

from init_db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT * FROM users LIMIT 5;")
print("Users:", cur.fetchall())

cur.execute("SELECT * FROM orders LIMIT 5;")
print("Orders:", cur.fetchall())

cur.close()
conn.close()

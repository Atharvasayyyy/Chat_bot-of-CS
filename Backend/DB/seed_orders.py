# db/seed_orders.py

from init_db import get_connection
import random

products = [
    ("Fan", 2500),
    ("Laptop", 55000),
    ("Shoes", 3000),
    ("Phone", 20000),
    ("Headphones", 1500)
]

def seed_orders():
    conn = get_connection()
    cur = conn.cursor()

    order_id_counter = 1

    for i in range(1, 51):
        user_id = f"U{i:03}"

        for _ in range(random.randint(1, 3)):
            product, price = random.choice(products)
            order_id = f"O{order_id_counter:04}"

            cur.execute("""
            INSERT INTO orders (order_id, user_id, product_name, price, status)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING
            """, (order_id, user_id, product, price, "delivered"))

            order_id_counter += 1

    conn.commit()
    cur.close()
    conn.close()

seed_orders()
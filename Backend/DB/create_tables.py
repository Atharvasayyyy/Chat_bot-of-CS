# db/create_tables.py

from init_db import get_connection


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    try:
        # ==================================================
        # USERS TABLE
        # ==================================================
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR PRIMARY KEY,
            name VARCHAR,
            email VARCHAR,
            complaint_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("✅ Users table ready")

        # ==================================================
        # ORDERS TABLE
        # ==================================================
        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            product_name VARCHAR,
            price FLOAT,
            status VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)
        print("✅ Orders table ready")

        # ==================================================
        # TICKETS TABLE
        # ==================================================
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id SERIAL PRIMARY KEY,
            user_id VARCHAR,
            order_id VARCHAR,
            issue TEXT,
            status VARCHAR,
            priority VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("✅ Tickets table ready")

        # ==================================================
        # EXCHANGES TABLE
        # ==================================================
        cur.execute("""
        CREATE TABLE IF NOT EXISTS exchanges (
            exchange_id SERIAL PRIMARY KEY,
            user_id VARCHAR,
            order_id VARCHAR,
            new_product VARCHAR,
            status VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("✅ Exchanges table ready")

        # ==================================================
        # 🔥 REFUNDS TABLE (IMPORTANT FIX)
        # ==================================================
        cur.execute("""
        CREATE TABLE IF NOT EXISTS refunds (
            refund_id SERIAL PRIMARY KEY,
            user_id VARCHAR,
            order_id VARCHAR,
            reason TEXT,
            status VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("✅ Refunds table ready")

        # Commit everything
        conn.commit()

    except Exception as e:
        print("❌ DB Table Creation Error:", e)

    finally:
        cur.close()
        conn.close()


# Run once
if __name__ == "__main__":
    create_tables()
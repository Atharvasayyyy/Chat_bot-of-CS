# DB/clear_data.py
# Script to clear all data from refunds, exchanges, and tickets tables

from init_db import get_connection


def clear_all_data():
    """Clear all data from refunds, exchanges, and tickets tables"""
    conn = get_connection()
    cur = conn.cursor()

    try:
        print("🗑️ Clearing data from tables...")

        # Clear tickets table
        cur.execute("DELETE FROM tickets;")
        print("✅ Tickets table cleared")

        # Clear exchanges table
        cur.execute("DELETE FROM exchanges;")
        print("✅ Exchanges table cleared")

        # Clear refunds table
        cur.execute("DELETE FROM refunds;")
        print("✅ Refunds table cleared")

        # Commit changes
        conn.commit()
        print("\n🎉 All data cleared successfully!")

    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        conn.rollback()

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    clear_all_data()

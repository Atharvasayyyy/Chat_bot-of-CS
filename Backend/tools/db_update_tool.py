# tools/db_update_tool.py
# increment when the user has filed the complaint and we need to update the complaint count in the user table

from langchain.tools import tool
from services.db_service import get_connection

@tool
def increment_complaint(user_id: str) -> str:
    """
    Increment complaint count when a new issue is raised.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET complaint_count = complaint_count + 1
        WHERE user_id = %s
    """, (user_id,))

    conn.commit()

    cur.close()
    conn.close()

    return "Complaint count updated"
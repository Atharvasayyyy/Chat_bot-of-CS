# tools/log_tool.py
from langchain.tools import tool
from services.db_service import execute_query

@tool
def log_action(action: str, user_id: str) -> str:
    """
    Log system action.
    """

    query = """
    INSERT INTO logs (user_id, action)
    VALUES (%s, %s)
    """

    execute_query(query, (user_id, action))

    return "Action logged"
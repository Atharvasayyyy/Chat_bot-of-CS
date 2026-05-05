# logic/agent.py

import json
import re

from services.llm_service01 import call_groq
from services.llm_service02 import call_mistral
from logic.prompts.system_prompt import SYSTEM_PROMPT
from tools import ALL_TOOLS

# 🧠 In-memory conversation store
USER_MEMORY = {}


# 🔹 LLM Router
def get_llm(use_case="general"):
    if use_case in ["refund", "exchange"]:
        return call_mistral
    return call_groq


# 🔹 Tool Executor
def run_tool(tool_name, tool_args):
    for tool in ALL_TOOLS:
        if tool.name == tool_name:
            print(f"🔧 EXECUTING TOOL: {tool_name}")
            return tool.run(tool_args)
    return "Tool not found"


# 🔹 Extract tool call from LLM output
def extract_tool_call(text):
    try:
        match = re.search(
            r'functions\.(\w+):\d+.*?{(.*?)}',
            text,
            re.DOTALL
        )
        if not match:
            return None, None

        tool_name = match.group(1)
        args_str = "{" + match.group(2) + "}"

        args = json.loads(args_str)
        return tool_name, args

    except Exception as e:
        print("❌ Tool parse error:", e)
        return None, None


# 🔹 Main Agent Logic
def run_agent(user_id, user_input, use_case="general"):
    llm = get_llm(use_case)

    # 🧠 Get memory (limit last 10 messages)
    history = USER_MEMORY.get(user_id, [])[-10:]

    # Add current user message
    history.append({"role": "user", "content": user_input})

    # Build prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history
    ]

    # 🔹 Step 1: LLM call
    response = llm(messages)

    print("🧠 LLM RESPONSE:", response)

    # 🔹 Step 2: Check for tool call
    tool_name, tool_args = extract_tool_call(response)

    if tool_name:
        print(f"🔧 TOOL REQUESTED: {tool_name}")

        # 🔥 Inject user_id if missing
        if isinstance(tool_args, dict) and "user_id" not in tool_args:
            tool_args["user_id"] = user_id

        tool_result = run_tool(tool_name, tool_args)

        # 🔹 Step 3: Send tool result back to LLM
        followup_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "assistant", "content": response},
            {
                "role": "user",
                "content": f"""
Tool result:
{tool_result}

Now give final response to the user.
"""
            }
        ]

        final_response = llm(followup_messages)

    else:
        final_response = response

    # 🧠 Save memory
    history.append({"role": "assistant", "content": final_response})
    USER_MEMORY[user_id] = history

    return final_response


# 🔹 Builder (kept same)
def create_agent(user_id, use_case="general"):
    return lambda user_input: run_agent(user_id, user_input, use_case)

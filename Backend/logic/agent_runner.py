from logic.agent import create_agent
from logic.memory import add_to_memory


def run_agent(user_id, user_input, use_case):

    agent = create_agent(user_id, use_case)

    add_to_memory(user_id, "user", user_input)

    try:
        response = agent(user_input)

        # 🔥 CLEAN RESPONSE
        if isinstance(response, str):
            if len(response) > 300:
                response = response[:300]

    except Exception as e:
        print("🔥 Agent Error:", e)
        return "Something went wrong."

    add_to_memory(user_id, "assistant", response)

    return response
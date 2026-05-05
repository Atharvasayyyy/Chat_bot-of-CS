# logic/decision.py

def decide_flow(intent, risk):
    if intent == "refund":
        if risk == "high":
            return "ticket"
        return "refund"

    if intent == "exchange":
        return "exchange"

    return "query"
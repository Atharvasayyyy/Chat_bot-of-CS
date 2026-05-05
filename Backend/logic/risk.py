# logic/risk.py

def classify_risk(evidence, image_data=None, context=None):
    """
    context:
    {
        "price": float,
        "kb_found": bool,
        "user_history": int (number of past complaints)
    }
    """

    score = 0

    # 🔹 1. Image similarity (CLIP)
    if image_data:
        similarity = image_data.get("similarity")
        if similarity is not None:
            if similarity < 0.6:
                score += 3   # very risky
            elif similarity < 0.8:
                score += 1

    # 🔹 2. AI-generated image (Hive)
    if image_data:
        ai_flag = image_data.get("ai_score")
        if ai_flag and ai_flag.get("confidence", 0) > 0.7:
            score += 3

    # 🔹 3. Missing image
    if not evidence.get("has_image"):
        score += 2

    # 🔹 4. Description quality
    if evidence.get("description_quality") == "low":
        score += 1

    # 🔹 5. Product price
    if context:
        price = context.get("price", 0)
        if price > 10000:
            score += 3
        elif price > 5000:
            score += 2

    # 🔹 6. Knowledge base availability
    if context and context.get("kb_found") is False:
        score += 2

    # 🔹 7. User history (fraud signal)
    if context:
        complaints = context.get("user_history", 0)
        if complaints > 3:
            score += 3
        elif complaints > 1:
            score += 1

    # 🔥 FINAL DECISION
    if score >= 6:
        return "high"
    elif score >= 3:
        return "medium"
    return "low"
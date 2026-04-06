# grader.py
# Advanced grading system with granular scoring (0.1 increments)
# Evaluates: correctness, politeness, completeness, emotional handling
# Penalizes: short, irrelevant, or rude responses


def grade_response(task, response):
    # ✅ fix dict issue
    if isinstance(response, dict):
        response = response.get("content", str(response))

    response_lower = response.lower()

    breakdown = {
        "correctness": 0.0,
        "politeness": 0.0,
        "completeness": 0.0,
        "emotion": 0.0,
        "penalties": 0.0
    }

    for word in task["expected_keywords"]:
        if word in response_lower:
            breakdown["correctness"] += 0.1

    if any(w in response_lower for w in ["sorry", "apologize", "thank"]):
        breakdown["politeness"] += 0.2

    if any(w in response_lower for w in ["refund", "return", "delivery", "order"]):
        breakdown["completeness"] += 0.2

    if task["mood"] == "angry" and "sorry" in response_lower:
        breakdown["emotion"] += 0.2

    total = sum(breakdown.values())
    total = max(0.0, min(1.0, total))

    return round(total, 2), breakdown

    
    # ═══════════════════════════════════════════════════
    # FINAL SCORE
    # ═══════════════════════════════════════════════════
    total = (
        breakdown["correctness"]
        + breakdown["politeness"]
        + breakdown["completeness"]
        + breakdown["emotion"]
        + breakdown["penalties"]
    )

    # bonus for decisive action
    if "will" in response_lower or "immediately" in response_lower:
        total += 0.1

    # Clamp and round to 0.1 increments
    total = max(0.0, min(1.0, total))
    total = round(total, 1)

    return total, breakdown

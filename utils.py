# utils.py
def generate_reason(skill):
    reasons = []

    if skill["demand"] < 0.4:
        reasons.append("low demand")
    if skill["growth"] < 0.4:
        reasons.append("declining trend")
    if skill["competition"] > 0.7:
        reasons.append("high competition")
    if skill["score"] < 0.3:
        reasons.append("low overall value")

    return ", ".join(reasons)


def classify_skill(skill):
    if skill["score"] > 0.4:
        return "invest"
    elif skill["score"] > 0.2:
        return "reduce"
    else:
        return "avoid"
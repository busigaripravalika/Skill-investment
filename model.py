# model.py
WEIGHTS = {
    "demand": 0.3,
    "salary": 0.25,
    "growth": 0.2,
    "synergy": 0.15,
    "competition": -0.1
}

def compute_score(skill):
    return (
        skill["demand"] * WEIGHTS["demand"] +
        skill["salary"] * WEIGHTS["salary"] +
        skill["growth"] * WEIGHTS["growth"] +
        skill["synergy"] * WEIGHTS["synergy"] +
        skill["competition"] * WEIGHTS["competition"]
    )

def compute_risk(skill):
    risk = 0

    if skill["growth"] < 0.4:
        risk += 0.4
    if skill["competition"] > 0.7:
        risk += 0.3
    if skill["demand"] < 0.4:
        risk += 0.3

    return min(risk, 1)

def allocate_time(skills, total_time):
    total_score = sum(s["score"] for s in skills if s["score"] > 0)

    for s in skills:
        if s["score"] > 0:
            s["allocated_time"] = (s["score"] / total_score) * total_time
        else:
            s["allocated_time"] = 0

    return skills

def process_skills(skills, total_time):
    for s in skills:
        s["score"] = compute_score(s)
        s["risk"] = compute_risk(s)

    skills = allocate_time(skills, total_time)
    skills.sort(key=lambda x: x["score"], reverse=True)

    return skills
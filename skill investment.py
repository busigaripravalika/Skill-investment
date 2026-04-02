import streamlit as st
st.title("Skill Investment + Avoidance Engine (Advanced Version)")
WEIGHTS = {
    "demand": 0.3,
    "salary": 0.25,
    "growth": 0.2,
    "synergy": 0.15,
    "competition": -0.1  # negative impact
}
def compute_score(skill):
    score = (
        skill["demand"] * WEIGHTS["demand"] +
        skill["salary"] * WEIGHTS["salary"] +
        skill["growth"] * WEIGHTS["growth"] +
        skill["synergy"] * WEIGHTS["synergy"] +
        skill["competition"] * WEIGHTS["competition"]
    )
    return score


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

st.sidebar.header("User Input")
total_time = st.sidebar.slider("Available Time", 1.0, 10.0, 5.0)

skill_names = ["Python", "Java", "React", "HTML", "jQuery", "AI/ML"]

skills = []

st.subheader("Enter Skill Metrics (0–1 scale)")

for name in skill_names:
    st.markdown(f"### {name}")
    col1, col2, col3 = st.columns(3)

    with col1:
        demand = st.slider(f"{name} Demand", 0.0, 1.0, 0.7, key=name+"d")
        salary = st.slider(f"{name} Salary", 0.0, 1.0, 0.7, key=name+"s")

    with col2:
        growth = st.slider(f"{name} Growth", 0.0, 1.0, 0.7, key=name+"g")
        competition = st.slider(f"{name} Competition", 0.0, 1.0, 0.5, key=name+"c")

    with col3:
        synergy = st.slider(f"{name} Synergy", 0.0, 1.0, 0.7, key=name+"sy")

    skill = {
        "name": name,
        "demand": demand,
        "salary": salary,
        "growth": growth,
        "competition": competition,
        "synergy": synergy
    }

    skills.append(skill)
if st.button("Analyze Portfolio"):
    for s in skills:
        s["score"] = compute_score(s)
        s["risk"] = compute_risk(s)
    skills = allocate_time(skills, total_time)
    skills.sort(key=lambda x: x["score"], reverse=True)

    st.subheader("📈 Investment Recommendations")

    for s in skills:
        if s["score"] > 0.4:
            st.success(
                f"{s['name']} → Invest | Time: {round(s['allocated_time'],2)} hrs | "
                f"Score: {round(s['score'],2)} | Risk: {round(s['risk'],2)}"
            )

    st.subheader("⚠️ Reduce / Moderate Investment")

    for s in skills:
        if 0.2 < s["score"] <= 0.4:
            st.warning(
                f"{s['name']} → Reduce | Score: {round(s['score'],2)} | "
                f"Reason: moderate returns"
            )

    st.subheader("❌ Avoid Learning")

    for s in skills:
        if s["score"] <= 0.2:
            reason = generate_reason(s)
            st.error(
                f"{s['name']} → Avoid because {reason}"
            )
    st.subheader("Skill Score Distribution")
    chart_data = {s["name"]: s["score"] for s in skills}
    st.bar_chart(chart_data)
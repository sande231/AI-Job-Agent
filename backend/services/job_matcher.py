USER_SKILLS = [
    "python",
    "fastapi",
    "javascript",
    "react",
    "machine learning",
    "generative ai",
    "git",
    "github",
    "docker",
    "mysql"
]


def analyze_job(description: str, user_skills: list[str]):

    description = description.lower()

    matched_skills = []
    missing_skills = []

    for skill in user_skills:
        skill_lower = skill.lower()

        if skill_lower in description:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_percentage = (
        len(matched_skills) / len(user_skills)
    ) * 100

    if match_percentage >= 80:
        recommendation = "Strong Match"

    elif match_percentage >= 60:
        recommendation = "Good Match"

    elif match_percentage >= 40:
        recommendation = "Possible Match"

    else:
        recommendation = "Weak Match"

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_count": len(matched_skills),
        "match_percentage": round(match_percentage, 2),
        "recommendation": recommendation
    }
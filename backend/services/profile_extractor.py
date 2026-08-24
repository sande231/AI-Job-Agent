def extract_basic_profile(resume_text: str):

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    name = "Unknown"

    if lines:
        name = lines[0]

    education = "Not detected"

    for line in lines:
        line_lower = line.lower()

        if (
            "bachelor" in line_lower
            or "computer science" in line_lower
            or "university" in line_lower
        ):
            education = line
            break

    return {
        "name": name,
        "education": education
    }
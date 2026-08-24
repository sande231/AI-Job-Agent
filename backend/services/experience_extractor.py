def extract_experience(resume_text: str):

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    experience_lines = []

    keywords = [
        "assistant",
        "intern",
        "engineer",
        "developer",
        "research",
        "manager",
        "analyst"
    ]

    for line in lines:
        line_lower = line.lower()

        for keyword in keywords:
            if keyword in line_lower:
                experience_lines.append(line)
                break

    return experience_lines
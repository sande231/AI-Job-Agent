def extract_projects(resume_text: str):

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    project_lines = []

    keywords = [
        "project",
        "dashboard",
        "agent",
        "recommendation",
        "study buddy",
        "expense tracker",
        "navigator",
        "application"
    ]

    for line in lines:
        line_lower = line.lower()

        for keyword in keywords:
            if keyword in line_lower:
                project_lines.append(line)
                break

    return project_lines
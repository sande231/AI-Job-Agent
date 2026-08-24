COMMON_SKILLS = {
    "python": "Python",
    "fastapi": "FastAPI",
    "javascript": "JavaScript",
    "react": "React",
    "vite": "Vite",
    "tailwind css": "Tailwind CSS",
    "rest api": "REST API",
    "machine learning": "Machine Learning",
    "generative ai": "Generative AI",
    "ai agents": "AI Agents",
    "rag": "RAG",
    "gemini": "Gemini",
    "google adk": "Google ADK",
    "vertex ai": "Vertex AI",
    "mysql": "MySQL",
    "redis": "Redis",
    "docker": "Docker",
    "google cloud": "Google Cloud",
    "git": "Git",
    "github": "GitHub",
    "sql": "SQL",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn"
}


def extract_skills(resume_text: str):

    text = resume_text.lower()

    detected_skills = []

    for keyword, display_name in COMMON_SKILLS.items():
        if keyword in text:
            detected_skills.append(display_name)

    return detected_skills
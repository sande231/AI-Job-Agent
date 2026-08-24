import os

import requests
from dotenv import load_dotenv


load_dotenv()


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

ADZUNA_BASE_URL = (
    "https://api.adzuna.com/v1/api/jobs/us/search"
)


def get_sample_internships():
    jobs = [
        {
            "title": "Software Engineering Intern",
            "company": "Future Tech",
            "description": (
                "Looking for a computer science student with "
                "Python, Git, REST API, Docker, and SQL experience."
            ),
            "location": "Remote",
            "job_url": (
                "https://example.com/jobs/"
                "software-engineering-intern"
            ),
            "source": "Sample Jobs",
        },
        {
            "title": "Machine Learning Intern",
            "company": "AI Labs",
            "description": (
                "Seeking an intern with Python, machine learning, "
                "NumPy, Pandas, Scikit-learn, and Git experience."
            ),
            "location": "New York, NY",
            "job_url": "https://example.com/jobs/ml-intern",
            "source": "Sample Jobs",
        },
        {
            "title": "Frontend Developer Intern",
            "company": "Web Systems",
            "description": (
                "Looking for React, JavaScript, CSS, HTML, "
                "and frontend development experience."
            ),
            "location": "Remote",
            "job_url": "https://example.com/jobs/frontend-intern",
            "source": "Sample Jobs",
        },
    ]

    return jobs


def search_internships(
    keyword="software engineering intern",
    results_per_page=10,
):
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError(
            "Adzuna API credentials were not found."
        )

    url = f"{ADZUNA_BASE_URL}/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": keyword,
        "content-type": "application/json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    discovered_jobs = []

    for job in data.get("results", []):
        company_data = job.get("company") or {}
        location_data = job.get("location") or {}

        discovered_jobs.append({
            "title": job.get(
                "title",
                "Unknown Position",
            ),
            "company": company_data.get(
                "display_name",
                "Unknown Company",
            ),
            "description": job.get(
                "description",
                "",
            ),
            "location": location_data.get(
                "display_name",
                "",
            ),
            "job_url": job.get(
                "redirect_url",
                "",
            ),
            "source": "Adzuna",
        })

    return discovered_jobs

def search_multiple_internship_categories(
    results_per_category=3,
):
    keywords = [
        "software engineering intern",
        "AI intern",
        "machine learning intern",
        "generative AI intern",
        #"data science intern",
        #"backend engineering intern",
        #"Python intern",
    ]

    all_jobs = []
    seen_urls = set()

    for keyword in keywords:
        jobs = search_internships(
            keyword=keyword,
            results_per_page=results_per_category,
        )

        for job in jobs:
            job_url = job.get("job_url")

            if not job_url:
                continue

            if job_url in seen_urls:
                continue

            seen_urls.add(job_url)

            job["search_keyword"] = keyword

            all_jobs.append(job)

    return all_jobs
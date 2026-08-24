from services.application_matcher import match_email_to_application
from services.email_classifier import classify_job_email


applications = [
    {
        "id": 2,
        "title": "AI Engineer Intern",
        "company": "Future AI",
        "status": "Applied",
    },
    {
        "id": 3,
        "title": "AI Intern",
        "company": "Example Tech",
        "status": "Applied",
    },
]


fake_email = {
    "from": "Example Tech Recruiting <recruiting@exampletech.com>",
    "subject": "Interview Invitation - AI Intern",
    "snippet": (
        "We would like to interview you for the AI Intern "
        "position at Example Tech."
    ),
}


match = match_email_to_application(
    fake_email,
    applications,
)

status = classify_job_email(fake_email)


print("Detected Status:", status)

if match:
    print("Matched Application ID:", match["application"]["id"])
    print("Company:", match["application"]["company"])
    print("Title:", match["application"]["title"])
    print("Match Score:", match["match_score"])
else:
    print("No matching application found.")
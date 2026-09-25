from services.application_matcher import match_email_to_application
from services.email_classifier import classify_job_email


APPLICATIONS = [
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


def test_matches_email_to_correct_application():
    email = {
        "from": "Example Tech Recruiting <recruiting@exampletech.com>",
        "subject": "Interview Invitation - AI Intern",
        "snippet": (
            "We would like to interview you for the AI Intern "
            "position at Example Tech."
        ),
    }

    result = match_email_to_application(email, APPLICATIONS)

    assert result is not None
    assert result["application"]["id"] == 3
    assert result["application"]["company"] == "Example Tech"
    assert result["match_score"] > 0


def test_classifies_interview_email():
    email = {
        "from": "Example Tech Recruiting <recruiting@exampletech.com>",
        "subject": "Interview Invitation - AI Intern",
        "snippet": (
            "We would like to interview you for the AI Intern "
            "position at Example Tech."
        ),
    }

    assert classify_job_email(email) == "Interview"


def test_returns_none_when_no_application_matches():
    email = {
        "from": "noreply@unrelated.com",
        "subject": "Newsletter",
        "snippet": "Weekly newsletter roundup for our subscribers.",
    }

    assert match_email_to_application(email, APPLICATIONS) is None

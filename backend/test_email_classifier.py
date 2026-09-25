import pytest

from services.email_classifier import (
    is_job_related_email,
    classify_job_email,
)


CASES = [
    (
        {
            "subject": "Thank you for applying",
            "snippet": (
                "We received your application for the Software "
                "Engineering Intern position."
            ),
        },
        True,
        "Applied",
    ),
    (
        {
            "subject": "Online Assessment Invitation",
            "snippet": (
                "Please complete the online assessment for your "
                "internship application."
            ),
        },
        True,
        "Assessment",
    ),
    (
        {
            "subject": "Interview Invitation",
            "snippet": "We would like to interview you for the AI Intern position.",
        },
        True,
        "Interview",
    ),
    (
        {
            "subject": "Application Update",
            "snippet": (
                "Unfortunately, we have decided not to move forward "
                "with your application."
            ),
        },
        True,
        "Rejected",
    ),
    (
        {
            "subject": "Job Offer",
            "snippet": "We are pleased to offer you the Software Engineering Intern position.",
        },
        True,
        "Offer",
    ),
    (
        {
            "subject": "70% OFF Today",
            "snippet": "Shop our latest deals and free shipping.",
        },
        False,
        None,
    ),
]


@pytest.mark.parametrize("email,expected_related,expected_status", CASES)
def test_classifies_email(email, expected_related, expected_status):
    related = is_job_related_email(email)

    assert related is expected_related

    if related:
        assert classify_job_email(email) == expected_status

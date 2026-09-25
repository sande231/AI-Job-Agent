from services.date_extractor import (
    extract_interview_date,
    normalize_interview_date,
)


def test_extracts_month_name_date_from_snippet():
    email = {
        "subject": "Interview Invitation - Example Tech AI Intern",
        "snippet": (
            "We would like to interview you on August 20, 2026 "
            "at 2:00 PM for the AI Intern position."
        ),
    }

    assert extract_interview_date(email) == "August 20, 2026 at 2:00 PM"


def test_extracts_slash_format_date():
    email = {
        "subject": "Interview",
        "snippet": "Please join us on 08/20/2026 at 2:00 PM.",
    }

    assert extract_interview_date(email) == "08/20/2026 at 2:00 PM"


def test_returns_none_when_no_date_found():
    email = {
        "subject": "Application received",
        "snippet": "Thanks for applying, we will be in touch soon.",
    }

    assert extract_interview_date(email) is None


def test_normalize_interview_date_produces_iso_like_string():
    normalized = normalize_interview_date("August 20, 2026 at 2:00 PM")

    assert normalized == "2026-08-20 14:00:00"

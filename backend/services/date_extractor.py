import re
from datetime import datetime


def extract_interview_date(email):
    subject = email.get("subject", "")
    snippet = email.get("snippet", "")

    text = f"{subject} {snippet}"

    patterns = [
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s+\d{4}\s+at\s+\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)",
        r"\b\d{1,2}/\d{1,2}/\d{4}\s+at\s+\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return None


def normalize_interview_date(date_text):
    if not date_text:
        return None

    formats = [
        "%B %d, %Y at %I:%M %p",
        "%b %d, %Y at %I:%M %p",
        "%m/%d/%Y at %I:%M %p",
    ]

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(
                date_text,
                date_format,
            )

            return parsed_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except ValueError:
            continue

    return None
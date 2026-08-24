from datetime import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def is_within_24_hours(interview_date: str):
    if not interview_date:
        return False

    try:
        interview_datetime = datetime.strptime(
            interview_date,
            DATE_FORMAT,
        )
    except ValueError:
        return False

    now = datetime.now()

    time_difference = interview_datetime - now

    hours_remaining = (
        time_difference.total_seconds() / 3600
    )

    return 0 < hours_remaining <= 24


def get_hours_until_interview(interview_date: str):
    if not interview_date:
        return None

    try:
        interview_datetime = datetime.strptime(
            interview_date,
            DATE_FORMAT,
        )
    except ValueError:
        return None

    now = datetime.now()

    time_difference = interview_datetime - now

    return round(
        time_difference.total_seconds() / 3600,
        2,
    )
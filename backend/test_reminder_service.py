from datetime import datetime, timedelta

from services.reminder_service import (
    is_within_24_hours,
    get_hours_until_interview,
)


tomorrow = datetime.now() + timedelta(hours=20)

test_date = tomorrow.strftime(
    "%Y-%m-%d %H:%M:%S"
)


print("Test Interview:", test_date)

print(
    "Within 24 Hours:",
    is_within_24_hours(test_date),
)

print(
    "Hours Remaining:",
    get_hours_until_interview(test_date),
)
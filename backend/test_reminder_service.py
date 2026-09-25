from datetime import datetime, timedelta

from services.reminder_service import (
    is_within_24_hours,
    get_hours_until_interview,
)


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _future(hours):
    return (datetime.now() + timedelta(hours=hours)).strftime(DATE_FORMAT)


def test_within_24_hours_true_for_near_future():
    assert is_within_24_hours(_future(20)) is True


def test_within_24_hours_false_for_far_future():
    assert is_within_24_hours(_future(48)) is False


def test_within_24_hours_false_for_past():
    assert is_within_24_hours(_future(-1)) is False


def test_within_24_hours_false_for_none_or_bad_input():
    assert is_within_24_hours(None) is False
    assert is_within_24_hours("not-a-date") is False


def test_hours_until_interview_close_to_20():
    hours = get_hours_until_interview(_future(20))
    assert 19.9 <= hours <= 20.1


def test_hours_until_interview_none_for_bad_input():
    assert get_hours_until_interview(None) is None
    assert get_hours_until_interview("not-a-date") is None

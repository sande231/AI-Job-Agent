from apscheduler.schedulers.background import BackgroundScheduler

from database.database import (
    get_upcoming_interviews,
    is_interview_reminder_sent,
    mark_interview_reminder_sent,
    get_application_summary,
    get_upcoming_events,
)

from services.email_service import (
    build_interview_reminder,
    build_application_report,
    send_email,
)

from services.reminder_service import (
    is_within_24_hours,
    get_hours_until_interview,
)


scheduler = BackgroundScheduler()


def check_interview_reminders():
    interviews = get_upcoming_interviews()

    for interview in interviews:
        interview_date = interview["interview_date"]

        if not is_within_24_hours(interview_date):
            continue

        if is_interview_reminder_sent(
            interview["id"],
            interview_date,
            "24_hour",
        ):
            continue

        hours_remaining = get_hours_until_interview(
            interview_date
        )

        reminder = build_interview_reminder(
            interview
        )

        send_email(
            to_email="Sandeepshah2054@gmail.com",
            subject=(
                f"Interview Reminder - "
                f"{interview['company']} "
                f"{interview['title']}"
            ),
            body=reminder,
        )

        mark_interview_reminder_sent(
            interview["id"],
            interview_date,
            "24_hour",
        )

        print(
            f"Reminder sent for {interview['company']} "
            f"- {hours_remaining} hours remaining"
        )


def send_daily_application_report():
    summary = get_application_summary()
    events = get_upcoming_events()

    report = build_application_report(
        summary,
        events,
    )

    send_email(
        to_email="Sandeepshah2054@gmail.com",
        subject="AI Job Agent - Daily Internship Report",
        body=report,
    )

    print("Daily application report sent.")


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            check_interview_reminders,
            "interval",
            hours=1,
            id="interview_reminder_check",
            replace_existing=True,
        )

        scheduler.add_job(
            send_daily_application_report,
            "cron",
            hour=8,
            minute=0,
            id="daily_application_report",
            replace_existing=True,
        )

        scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
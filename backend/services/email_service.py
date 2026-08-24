import base64
import os
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def get_gmail_service():
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES,
        )

    if not credentials or not credentials.valid:

        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )

            credentials = flow.run_local_server(
                port=0
            )

        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    return service


def build_application_report(summary, events):
    report = """
AI JOB AGENT - INTERNSHIP REPORT

APPLICATION SUMMARY
-------------------
"""

    report += f"Total Applications: {summary['total']}\n"
    report += f"Saved: {summary['Saved']}\n"
    report += f"Applied: {summary['Applied']}\n"
    report += f"Assessments: {summary['Assessment']}\n"
    report += f"Interviews: {summary['Interview']}\n"
    report += f"Rejected: {summary['Rejected']}\n"
    report += f"Offers: {summary['Offer']}\n"

    report += """
UPCOMING EVENTS
---------------
"""

    if not events:
        report += "No upcoming interviews or deadlines.\n"

    else:
        for event in events:
            report += (
                f"\nCompany: {event['company']}\n"
                f"Position: {event['title']}\n"
                f"Status: {event['status']}\n"
            )

            if event["interview_date"]:
                report += (
                    f"Interview: {event['interview_date']}\n"
                )

            if event["deadline"]:
                report += (
                    f"Deadline: {event['deadline']}\n"
                )

    return report


def send_email(
    to_email: str,
    subject: str,
    body: str,
):
    service = get_gmail_service()

    message = EmailMessage()

    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    send_message = {
        "raw": encoded_message
    }

    result = (
        service.users()
        .messages()
        .send(
            userId="me",
            body=send_message,
        )
        .execute()
    )

    return {
        "message": "Email sent successfully",
        "gmail_message_id": result["id"],
    }


def get_recent_emails(max_results: int = 10):
    service = get_gmail_service()

    result = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results,
        )
        .execute()
    )

    messages = result.get("messages", [])

    emails = []

    for message in messages:
        message_data = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = message_data.get(
            "payload",
            {}
        ).get(
            "headers",
            []
        )

        email_info = {
            "id": message["id"],
            "from": "",
            "subject": "",
            "date": "",
            "snippet": message_data.get("snippet", ""),
        }

        for header in headers:
            name = header.get("name")
            value = header.get("value")

            if name == "From":
                email_info["from"] = value

            elif name == "Subject":
                email_info["subject"] = value

            elif name == "Date":
                email_info["date"] = value

        emails.append(email_info)

    return emails


def build_interview_reminder(interview):
    return f"""
AI JOB AGENT - INTERVIEW REMINDER

Company: {interview['company']}
Position: {interview['title']}
Status: {interview['status']}
Interview Date: {interview['interview_date']}

Prepare your resume, review the job description,
and be ready before the interview time.

Good luck!
"""
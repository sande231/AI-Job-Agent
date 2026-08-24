from services.date_extractor import extract_interview_date


fake_email = {
    "subject": "Interview Invitation - Example Tech AI Intern",
    "snippet": (
        "We would like to interview you on August 20, 2026 "
        "at 2:00 PM for the AI Intern position."
    ),
}


date = extract_interview_date(fake_email)

print("Extracted Interview Date:", date)
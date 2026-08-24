from services.email_classifier import (
    is_job_related_email,
    classify_job_email,
)


test_emails = [
    {
        "subject": "Thank you for applying",
        "snippet": "We received your application for the Software Engineering Intern position."
    },
    {
        "subject": "Online Assessment Invitation",
        "snippet": "Please complete the online assessment for your internship application."
    },
    {
        "subject": "Interview Invitation",
        "snippet": "We would like to interview you for the AI Intern position."
    },
    {
        "subject": "Application Update",
        "snippet": "Unfortunately, we have decided not to move forward with your application."
    },
    {
        "subject": "Job Offer",
        "snippet": "We are pleased to offer you the Software Engineering Intern position."
    },
    {
        "subject": "70% OFF Today",
        "snippet": "Shop our latest deals and free shipping."
    },
]


for email in test_emails:
    related = is_job_related_email(email)

    if related:
        status = classify_job_email(email)
    else:
        status = "Not Job Related"

    print("------------------------------")
    print("Subject:", email["subject"])
    print("Job Related:", related)
    print("Detected Status:", status)
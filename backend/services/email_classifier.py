JOB_KEYWORDS = [
    "application",
    "candidate",
    "recruiter",
    "recruiting",
    "internship",
    "interview",
    "assessment",
    "coding challenge",
    "offer letter",
    "job offer",
    "hiring team",
]


IGNORE_SUBJECTS = [
    "ai job agent - internship application report",
    "hello from synapse",
]


def should_ignore_email(email):
    subject = email.get("subject", "").lower()

    return any(
        ignored_subject in subject
        for ignored_subject in IGNORE_SUBJECTS
    )


def is_job_related_email(email):

    if should_ignore_email(email):
        return False

    subject = email.get("subject", "").lower()
    snippet = email.get("snippet", "").lower()

    text = subject + " " + snippet

    return any(
        keyword in text
        for keyword in JOB_KEYWORDS
    )


def classify_job_email(email):

    subject = email.get("subject", "").lower()
    snippet = email.get("snippet", "").lower()

    text = subject + " " + snippet

    # OFFER
    offer_phrases = [
        "pleased to offer you",
        "offer letter",
        "job offer",
        "offer of employment",
        "extend an offer",
    ]

    if any(phrase in text for phrase in offer_phrases):
        return "Offer"

    # REJECTION
    rejection_phrases = [
        "unfortunately",
        "not moving forward",
        "decided not to move forward",
        "other candidates",
        "regret to inform",
        "position has been filled",
    ]

    if any(phrase in text for phrase in rejection_phrases):
        return "Rejected"

    # INTERVIEW
    interview_phrases = [
        "invite you to interview",
        "schedule an interview",
        "interview invitation",
        "interview availability",
        "schedule a call with",
        "would like to interview",
        "move forward with an interview",
    ]

    if any(phrase in text for phrase in interview_phrases):
        return "Interview"

    # ASSESSMENT
    assessment_phrases = [
        "complete the assessment",
        "online assessment",
        "coding challenge",
        "technical assessment",
        "take-home assessment",
    ]

    if any(phrase in text for phrase in assessment_phrases):
        return "Assessment"

    # APPLICATION CONFIRMATION
    applied_phrases = [
        "thank you for applying",
        "application received",
        "received your application",
        "application confirmation",
        "thank you for your application",
    ]

    if any(phrase in text for phrase in applied_phrases):
        return "Applied"

    return "Other"
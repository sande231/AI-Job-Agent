import re


EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

PHONE_PATTERN = re.compile(
    r"(\+?1[\s\-.]?)?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}"
)

LINKEDIN_PATTERN = re.compile(
    r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+",
    re.IGNORECASE,
)


def extract_email(resume_text: str):
    match = EMAIL_PATTERN.search(resume_text or "")
    return match.group(0) if match else None


def extract_phone(resume_text: str):
    match = PHONE_PATTERN.search(resume_text or "")
    return match.group(0).strip() if match else None


def extract_linkedin_url(resume_text: str):
    match = LINKEDIN_PATTERN.search(resume_text or "")

    if not match:
        return None

    url = match.group(0)

    if not url.lower().startswith("http"):
        url = f"https://{url}"

    return url


def extract_contact_info(resume_text: str):
    return {
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "linkedin_url": extract_linkedin_url(resume_text),
    }

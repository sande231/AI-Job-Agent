def match_email_to_application(email, applications):
    subject = email.get("subject", "").lower()
    snippet = email.get("snippet", "").lower()
    sender = email.get("from", "").lower()

    email_text = f"{subject} {snippet} {sender}"

    best_match = None
    best_score = 0

    for application in applications:
        company = application.get("company", "").lower()
        title = application.get("title", "").lower()

        score = 0

        if company and company in email_text:
            score += 3

        if title and title in email_text:
            score += 2

        company_words = [
            word
            for word in company.split()
            if len(word) > 2
        ]

        for word in company_words:
            if word in email_text:
                score += 1

        title_words = [
            word
            for word in title.split()
            if len(word) > 3
        ]

        for word in title_words:
            if word in email_text:
                score += 1

        if score > best_score:
            best_score = score
            best_match = application

    if best_score == 0:
        return None

    return {
        "application": best_match,
        "match_score": best_score,
    }
saved_resume_profile = None
saved_resume_text = None


def save_resume_profile(profile, resume_text):
    global saved_resume_profile
    global saved_resume_text

    saved_resume_profile = profile
    saved_resume_text = resume_text


def get_resume_profile():
    return saved_resume_profile


def get_resume_text():
    return saved_resume_text
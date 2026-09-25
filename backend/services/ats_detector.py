import re


# Ordered roughly by how common these are in internship/new-grad
# postings. Add new platforms here as they show up in real
# discovered-job data - this is a starting set, not exhaustive.
PLATFORM_PATTERNS = {
    "greenhouse": [r"greenhouse\.io"],
    "lever": [r"lever\.co"],
    "workday": [r"myworkdayjobs\.com"],
    "icims": [r"icims\.com"],
    "smartrecruiters": [r"smartrecruiters\.com"],
    "ashby": [r"ashbyhq\.com"],
    "workable": [r"workable\.com"],
    "linkedin_easy_apply": [r"linkedin\.com/jobs"],
    "indeed": [r"indeed\.com"],
}

# Platforms that actually have a working prepare_application()
# adapter in services/apply_adapters/. Everything else gets
# detected (for visibility) but falls back to manual apply.
SUPPORTED_FOR_AUTO_APPLY = {"greenhouse", "lever"}


def detect_ats_platform(job_url):
    if not job_url:
        return "unknown"

    url = job_url.lower()

    for platform, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url):
                return platform

    return "unknown"


def is_supported_for_auto_apply(platform):
    return platform in SUPPORTED_FOR_AUTO_APPLY

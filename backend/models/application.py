from pydantic import BaseModel
from typing import Optional


class Application(BaseModel):
    title: str
    company: str
    description: str
    status: str = "Saved"

    job_url: Optional[str] = None
    match_score: Optional[int] = None
    location: Optional[str] = None
    date_applied: Optional[str] = None
    interview_date: Optional[str] = None
    deadline: Optional[str] = None
    notes: Optional[str] = None

    # Auto-apply tracking
    applied_via: Optional[str] = "manual"      # "manual" | "auto"
    ats_platform: Optional[str] = None          # "greenhouse", "lever", "unknown", ...
    submission_status: Optional[str] = None     # "prepared", "submitted", "manual_required", ...
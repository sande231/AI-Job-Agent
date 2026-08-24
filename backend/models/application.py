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
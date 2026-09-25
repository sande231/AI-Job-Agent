from pydantic import BaseModel
from typing import Optional


class ResumeProfile(BaseModel):
    name: str
    education: str
    career_goal: str
    skills: list[str]
    experience: list[str]
    projects: list[str]
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
from pydantic import BaseModel


class ResumeProfile(BaseModel):
    name: str
    education: str
    career_goal: str
    skills: list[str]
    experience: list[str]
    projects: list[str]
from pydantic import BaseModel


class Profile(BaseModel):
    name: str
    education: str
    career_goal: str
    skills: list[str]
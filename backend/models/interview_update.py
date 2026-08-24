from pydantic import BaseModel


class InterviewUpdate(BaseModel):
    interview_date: str
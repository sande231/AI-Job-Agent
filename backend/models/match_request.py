from pydantic import BaseModel

from models.job import Job
from models.profile import Profile


class MatchRequest(BaseModel):
    profile: Profile
    job: Job
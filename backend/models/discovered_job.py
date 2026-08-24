from typing import Optional

from pydantic import BaseModel


class DiscoveredJob(BaseModel):
    title: str
    company: str
    description: str

    location: Optional[str] = None
    job_url: Optional[str] = None
    source: Optional[str] = None

    match_score: Optional[int] = None

    status: str = "Discovered"
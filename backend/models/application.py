from pydantic import BaseModel


class Application(BaseModel):
    title: str
    company: str
    description: str
    status: str = "Saved"
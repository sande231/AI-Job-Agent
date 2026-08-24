from pydantic import BaseModel


class NotesUpdate(BaseModel):
    notes: str
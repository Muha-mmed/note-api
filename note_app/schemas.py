from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: Optional[str] | None = None

class CreateNote(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    owner: str
    created_at: datetime
    
    class Config:
        from_attributes: True
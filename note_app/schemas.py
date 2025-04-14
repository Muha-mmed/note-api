from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: Optional[str] | None = None

class CreateNote(NoteBase):
    pass

class UpdateNote(NoteBase):
    title: Optional[str] | None = None
    content: Optional[str] | None = None
    
class NoteResponse(BaseModel):
    id:int
    title: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes: True
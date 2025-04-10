
from sqlalchemy.orm import Session

from authentication.models import User
from note_app.models import Note
from note_app.schemas import CreateNote


def create_note_svc(note:CreateNote,db:Session,current_user:User):
    note = Note(
        title = note.title,
        content = note.content,
        owner_id = current_user.id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"message": "note added successfully"}

def get_note_svc(user: User,db:Session):
    note = db.query(Note).filter(Note.owner_id == user.id).all()
    if note == '':
        return {"message": "No note yet try add one"}
    return note
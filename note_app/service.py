
from sqlalchemy.orm import Session

from authentication.models import User
from note_app.models import Note
from note_app.schemas import CreateNote, UpdateNote


def create_note_svc(note:CreateNote,db:Session,current_user:User):
    note = Note(
        title = note.title,
        content = note.content,
        owner_email = current_user.email
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"message": "note added successfully"}

def get_note_svc(user: User,db:Session):
    note = db.query(Note).filter(Note.owner_email == user.email).all()
    if note == '' or note == []:
        return {"message": "No note yet try add one"}
    return note

def update_note_svc(note_data:UpdateNote,note_id:int,db:Session):
    note = db.query(Note).filter(Note.id == note_id).first()
    new_note = .
    
def delete_note_svc(note_id:int,user:User,db:Session):
    c_user = db.query(User).filter(User.email == user.email).first()
    note = db.query(Note).filter(Note.id == note_id).first()
    if  c_user.email != note.owner_email:
        return {"message": "request denied"}
    db.delete(note)
    db.commit()
    return {"message": "post deleted successfully"}
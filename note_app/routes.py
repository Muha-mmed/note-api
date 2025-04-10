from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session

from authentication.auth import JWTBearer, get_current_user
from authentication.models import User
from db import get_db

from note_app.service import create_note_svc,get_note_svc
from note_app.schemas import CreateNote


note_router = APIRouter(tags=["note"],prefix="/note")

@note_router.post("/create/note",status_code=201,dependencies = [Depends(JWTBearer())])
def create_note(note:CreateNote,db:Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    note = create_note_svc(note,db,current_user)
    if not note:
        raise HTTPException(status_code=401,detail="bad or invalid input")
    return {
        "message": "created",
        "data": note
    }
    
@note_router.get("/notes",status_code=200,dependencies = [Depends(JWTBearer())])
def get_note(current_user: User = Depends(get_current_user),db:Session= Depends(get_db)):
    note = get_note_svc(current_user,db)
    if not note:
        raise HTTPException(status_code=400,detail="No note yet try add one")
    return note
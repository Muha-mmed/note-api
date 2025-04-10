from fastapi import FastAPI
from authentication.routes import auth_route
from note_app.routes import note_router


app = FastAPI()

app.include_router(note_router)
app.include_router(auth_route)


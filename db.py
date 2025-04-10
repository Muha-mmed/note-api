from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config 

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
local_session = sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = local_session()
    try:
      yield db
    finally:
      db.close()
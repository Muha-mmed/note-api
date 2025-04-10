from sqlalchemy import Integer,String,Boolean,DateTime,Column,func,UUID
from sqlalchemy.orm import relationship
from db import Base,engine
from uuid import uuid4


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, unique=True, nullable=False)
    is_active = Column(Boolean, index=True, default=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    posts = relationship("note_app.models.Note",back_populates= "owner")    
    
Base.metadata.create_all(bind=engine)
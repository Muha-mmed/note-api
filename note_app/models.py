from sqlalchemy import Column, DateTime, Integer, String, Text, func,ForeignKey
from sqlalchemy.orm import relationship

from db import Base,engine

class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String, index=True,nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    owner_email = Column(String,ForeignKey("users.email"),nullable=False)

    owner = relationship("User",back_populates= "posts")
    
Base.metadata.create_all(bind=engine)
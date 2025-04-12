from typing import Optional
from pydantic import BaseModel
from src.infrastructure.database.connection_orm import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Notes(Base):
    __tablename__ = "notes"
    id_note = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    archived = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"))
    owner = relationship("User", back_populates="notes_user") #backpopulates define la relacion bidireccional
    active = Column(Boolean, nullable=False)
    category = relationship("Categories", back_populates="notes")
    category_id = Column(Integer, ForeignKey("categories.id_category", ondelete="CASCADE"))

class NoteCreate(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None
    
class NoteResponse(BaseModel):
    id_note: int
    archived: bool
    user_id: int
    active: bool
    class Config:
        from_attributes = True

class NoteEdit(NoteCreate):
    id_note: int
    archived: bool
    active: bool
    category_id: Optional[int] = None
    class Config:
        from_attributes = True

class NoteDelete(BaseModel):
    id_note: int

class NoteChangeStateArchived(BaseModel):
    id_note: int
    archived: bool

class NoteChangeStateActive(BaseModel):
    id_note: int
    active: bool

class NoteDeleteAddCategory(BaseModel):
    id_note: int
    category_id: int

class NoteFilterCategory(BaseModel):
    category_id: int
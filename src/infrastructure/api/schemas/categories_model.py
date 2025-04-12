from pydantic import BaseModel
from src.infrastructure.database.connection_orm import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Categories(Base):
    __tablename__ = "categories"
    id_category = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    notes = relationship("Notes", back_populates="category")

class CreateCategory(BaseModel):
    name: str
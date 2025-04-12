from fastapi import Depends, HTTPException
from src.infrastructure.database.connection_orm import get_db
from src.infrastructure.api.schemas import categories_model
from sqlalchemy.orm import Session

def create_category(category: categories_model.CreateCategory, db: Session = Depends(get_db)):
    db_category = categories_model.Categories(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql://postgres:36025147@localhost/fastapi') #8:54
print("Insertando usuario en base:", os.getenv("DATABASE_URL"))
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base() # crea una clase base a partir de la cual se definirán todos los modelos ORM.

async def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
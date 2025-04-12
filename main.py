from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infrastructure.api.controller.user_controller import router_user as user_router
from src.infrastructure.api.controller.notes_controller import router_notes as note_router
from src.infrastructure.api.controller.categories_controller import router_categories as category_router
from src.infrastructure.api.controller.auth import router_auth as auth_router
from src.infrastructure.api.schemas import user_model, notes_model, categories_model
from src.infrastructure.database.connection_orm import engine

user_model.Base.metadata.create_all(bind=engine)
notes_model.Base.metadata.create_all(bind=engine)
categories_model.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user_router)
app.include_router(note_router)
app.include_router(category_router)
app.include_router(auth_router)
@app.get("/")
async def root():
    return {"message": "Hello API"}
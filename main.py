from fastapi import FastAPI
from database.database import SessionLocal,engine
from database import models
from books import book_router

app = FastAPI()
app.include_router(book_router)

models.Base.metadata.create_all(bind=engine)




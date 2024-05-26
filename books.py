from sqlalchemy.orm import Session
from database.database import get_db
from pydantic import BaseModel,Field    
from database import models

from fastapi import APIRouter,Depends

book_router = APIRouter(prefix="/books")


class Book(BaseModel):
    name: str = Field(min_length=1,max_length=60)
    description: str = Field(min_length=1,max_length=200)
    author: str = Field(min_length=1,max_length=60)
    price: int = Field(gt=-1,lt=200)



@book_router.get("/")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@book_router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        return {"message":"404 not found"}
    return book

@book_router.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Book()
    book_model.name = book.name
    book_model.description = book.description
    book_model.author = book.author
    book_model.price = book.price

    db.add(book_model)
    db.commit()
    return book



@book_router.put("/{book_id}")
def update_book(book: Book,book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book_model is None:
        return {"message":"404 not found"}
    book_model.name = book.name
    book_model.description = book.description
    book_model.author = book.author
    book_model.price = book.price

    db.add(book_model)
    db.commit()
    return book



@book_router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book_model is None:
        return {"message":"404 not found"}
    db.query(models.Book).filter(models.Book.id == book_id).delete()
    db.commit()
    return {"message":"deleted"}
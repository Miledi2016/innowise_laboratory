from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional, List

#  Connecting to a database

# Using SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./book_collection.db"

# Creating a database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class that will be the database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining ORM models
Base = declarative_base()




# Defining a database and ORM model

# SQLAlchemy Model (DB Table Definition)
class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=True)


# Create all tables defined in Base
Base.metadata.create_all(bind=engine)


# Pydantic Data Validation Models (Schemas)

# Schema for creating/updating a book (input data)
class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: Optional[int] = Field(None, ge=1, le=2100)


# Read/respond schema (outgoing data, includes ID)
class Book(BookBase):
    id: int

    class Config:
        # Allows Pydantic to work with SQLAlchemy models
        from_attributes = True


# Creating a FastAPI Application

app = FastAPI(title="Book Collection API", version="1.0.0")




# Dependency for getting a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Adding endpoints

# Add a new book (POST /books/)
@app.post("/books/", response_model=Book, status_code=201, summary="Add a new book")
def create_book(book: BookBase, db: Session = Depends(get_db)):
    """
    Adds a new book to the collection.
    """
    db_book = DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book




# Get all books (GET /books/)
@app.get("/books/", response_model=List[Book], summary="Get all books with pagination")
def read_books(
        skip: int = Query(0, ge=0, description="Number of skipped records (offset)"),
        limit: int = Query(100, ge=1, le=100, description="Maximum number of books per page"),
        db: Session = Depends(get_db)
):
    """
    Gets a list of all books. Supports simple pagination with the `skip` and `limit` parameters.
    """
    books = db.query(DBBook).offset(skip).limit(limit).all()
    return books



# Search for books (GET /books/search/)
@app.get("/books/search/", response_model=List[Book], summary="Search books by title, author, or year")
def search_books(
        query: str = Query(..., min_length=1, description="Search string by title, author, or year"),
        db: Session = Depends(get_db)
):
    """
    Searches for books where the title, author, or year (converted to a string)
    contains the given string `query` (case-insensitive).
    """
    # Search by name
    search_title = DBBook.title.ilike(f"%{query}%")
    # Search by author
    search_author = DBBook.author.ilike(f"%{query}%")
    # Search by year (convert the year into a search string)
    search_year = DBBook.year.cast(String).ilike(f"%{query}%")

    books = db.query(DBBook).filter(
        search_title | search_author | search_year
    ).all()

    return books




# Update book details (PUT /books/{book_id})
@app.put("/books/{book_id}", response_model=Book, summary="Update book details by ID")
def update_book(
        book_id: int,
        book_update: BookBase,
        db: Session = Depends(get_db)
):
    """
    Updates an existing book by its ID.
    """
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    # Update fields, ignoring those that are not provided
    # Here we update all the fields, as BookBase requires title and author
    for key, value in book_update.model_dump(exclude_none=True).items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book



# Delete book (DELETE /books/{book_id})
@app.delete("/books/{book_id}", status_code=204, summary="Delete a book by ID")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Removes a book from the collection by its ID.
    """
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    db.delete(db_book)
    db.commit()
    # Status 204 No Content indicates success without a response body.
    return

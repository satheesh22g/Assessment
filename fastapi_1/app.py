from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
from pydantic import BaseModel
import sqlalchemy
# Database Configuration
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = sqlalchemy.orm.declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Define Book Model
class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)
    
    reviews = relationship("ReviewModel", back_populates="book")

# Define Review Model
class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    rating = Column(Integer)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("BookModel", back_populates="reviews")

Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for API validation
class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    text: str
    rating: int

# Background task for sending confirmation email (simulated)
def send_confirmation_email(review_id: int, email: str):
    # Simulated email sending process
    print(f"Sending confirmation email for review {review_id} to {email}")

# FastAPI app instance
app = FastAPI()

# CRUD operations for books
@app.post("/books/", response_model=Book)
def create_book(book: Book, db: Session = Depends(get_db)):
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[Book])
def read_books(author: Optional[str] = None, publication_year: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(BookModel)
    if author:
        query = query.filter(BookModel.author == author)
    if publication_year:
        query = query.filter(BookModel.publication_year == publication_year)
    return query.all()

# CRUD operations for reviews
@app.post("/reviews/", response_model=Review)
def create_review(review: Review, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_review = ReviewModel(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # Enqueue background task for sending confirmation email
    background_tasks.add_task(send_confirmation_email, db_review.id, "user@example.com")

    return db_review

@app.get("/reviews/{book_id}", response_model=List[Review])
def read_reviews(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return db_book.reviews

# Test Client
client = TestClient(app)

# Test cases
def test_create_book():
    response = client.post("/books/", json={"title": "Test Book", "author": "Test Author", "publication_year": 2022})
    assert response.status_code == 200

def test_create_review():
    response = client.post("/reviews/", json={"text": "Great book!", "rating": 5})
    assert response.status_code == 200

def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200

def test_read_reviews():
    response = client.get("/reviews/1")
    assert response.status_code == 200

# Run tests
if __name__ == "__main__":
    import pytest
    pytest.main([__file__])

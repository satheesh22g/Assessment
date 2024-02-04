# FastAPI Book Review System

## Overview
This project implements a simple RESTful API using FastAPI for a book review system. Users can add new books, submit reviews for books, and retrieve information about books and their reviews.

## Features

### Endpoints
1. **Add a New Book**
   - Endpoint: `/books/` (HTTP POST)
   - Parameters: `title`, `author`, `publication_year`

2. **Submit a Review for a Book**
   - Endpoint: `/reviews/` (HTTP POST)
   - Parameters: `text`, `rating`

3. **Retrieve All Books**
   - Endpoint: `/books/` (HTTP GET)
   - Optional Filters: `author`, `publication_year`

4. **Retrieve All Reviews for a Specific Book**
   - Endpoint: `/reviews/{book_id}` (HTTP GET)

### Data Validation
- Pydantic models are used for data validation in the API.

### Documentation
- Comments are included throughout the code for better understanding.
- FastAPI generates interactive API documentation, which can be accessed at `/docs` or `/redoc`.

### Error Handling
- Proper error handling is implemented for invalid requests.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the FastAPI application: `uvicorn app:app --reload`

## Running Tests
- Execute tests using  `pytest`.

 ``` python app.py```

 1. Q1
    FastAPI leverages asynchronous programming in Python through the use of asynchronous functions and the async and await keywords.
2. Q2
 the ability to inject dependencies, such as database connections or authentication mechanisms, into route handlers. It helps manage dependencies in a clean and organized manner.
3. Q3
   Code Walkthrough
1. Database Setup - SQLite database engine and a SessionLocal for managing database sessions.
2. setting up the FastAPI instance and defines a dependency get_db to get a database session.
3. Book Model and Review Model
4. CRUD Operations
5. Running the Application
   ```uvicorn app:app --reload```
   

  

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect("books.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
)
""")
conn.commit()

# Book model
class Book(BaseModel):
    title: str
    author: str
    year: int

# CRUD Endpoints
@app.post("/books/", response_model=Book)
def add_book(book: Book):
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                   (book.title, book.author, book.year))
    conn.commit()
    return book

@app.get("/books/", response_model=List[Book])
def list_books(order: Optional[str] = None):
    query = "SELECT title, author, year FROM books"
    if order == "asc":
        query += " ORDER BY year ASC"
    elif order == "desc":
        query += " ORDER BY year DESC"
    cursor.execute(query)
    books = cursor.fetchall()
    return [{"title": b[0], "author": b[1], "year": b[2]} for b in books]

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    cursor.execute("UPDATE books SET title=?, author=?, year=? WHERE id=?",
                   (book.title, book.author, book.year, book_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}

@app.get("/books/search/")
def search_books(title: Optional[str] = None, author: Optional[str] = None):
    query = "SELECT title, author, year FROM books WHERE 1=1"
    params = []
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if author:
        query += " AND author LIKE ?"
        params.append(f"%{author}%")
    
    cursor.execute(query, params)
    books = cursor.fetchall()
    return [{"title": b[0], "author": b[1], "year": b[2]} for b in books]

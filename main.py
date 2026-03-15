from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import  Optional

app = FastAPI()

# Homepage
@app.get('/')
def home():
    return {"message": "Library API, go to /books to look at available books."}

# DATA
users = [
    {"id": 1, "name": "Amy", "borrowed_books": [] },
    {"id": 2, "name": "Bob", "borrowed_books": [] },
    {"id": 3, "name": "Carey", "borrowed_books": [] },
    {"id": 4, "name": "Dan", "borrowed_books": [] }
]

titles = ["Don Quixote" ,"Alice's Adventures in Wonderland","The Adventures of Huckleberry Finn","The Adventures of Tom Sawyer","Treasure Island","Pride and Prejudice","Wuthering Heights","Jane Eyre","Moby Dick","The Scarlet Letter "
]

authors = ["Miguel de Cervantes","Lewis Carroll","Mark Twain","Mark Twain","Robert Louis Stevenson","Jane Austen","Emily Brontë","Charlotte Brontë","Herman Melville","Nathaniel Hawthorne"
]

books = [
    {
    "id": i + 1,
    "title": titles[i],
    "author": authors[i],
    "is_available": True,
    "due_date": None
} for i in range(len(titles))
]

# ROUTES
# GET: all books
@app.get('/books')
def get_books():
    return books

# GET: all users
@app.get('/users')
def get_users():
    return users

# POST: borrow a book
@app.post('/borrowbook')
def borrow_book(user_id: int, book_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    book = next((b for b in books if b["id"] == book_id), None)
    
    # raise error if not existing
    if not user or not book:
        raise HTTPException(status_code=404, detail="User of book does not exist.")

    if not book["is_available"]:
        raise HTTPException(status_code=400, detail="Book is not available.")

    if len(user["borrowed_books"]) >= 2:
        raise HTTPException(status_code=400, detail="Max Limit of borrowed books reached")
    
    # max 1 week lending window
    today = datetime.now()
    due_date = today + timedelta(days=7)
    
    # Update data
    book["is_available"] = False
    book["due_date"] = due_date.strftime("%a %b %d %Y") # weekday month day year
    user["borrowed_books"].append({
        "book_id": book["id"],
        "title": book["title"],
        "return_by": book["due_date"]
    })

    return {"message": "Done", "user": user}
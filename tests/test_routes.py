import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from models.book import Book
from models.user import User

client = TestClient(app) # Fake client

# FAKE DATA FOR MOCKING
FAKE_BOOKS = [
    Book(
    book_id=1, title="Don Quixote",
    author="Miguel de Cervantes",
    is_available=True, due_date=None
    ),
    Book(
    book_id=4, title="The Adventures of Tom Sawyer",
    author="Mark Twain",
    is_available=False, due_date="Sat Mar 21 2026"
    ),
    Book(
    book_id=5, title="Treasure Island",
    author="Robert Louis Stevenson",
    is_available=True, due_date=None
    )
]

FAKE_USERS = [
    User(user_id=1, name="Amy", borrowed_books=[]),
    User(user_id=3, name="Carey", borrowed_books=[
                    Book(book_id=3, title="The Adventures of Huckleberry Finn", due_date="Sat Mar 21 2026"),
                    Book(book_id=4, title="The Adventures of Tom Sawyer", due_date="Sat Mar 21 2026")
                   ]
    )
]

# books routes
# get routes
def test_get_all_books():
    with patch("routes.books.service.get_all_books", return_value=FAKE_BOOKS):
        response = client.get("/books/")
    
    assert response.status_code == 200
    
    assert len(response.json()) == 3
    assert response.json()[0]["title"] == "Don Quixote"

def test_get_book_found():
    with patch("routes.books.service.get_book_by_id", return_value=FAKE_BOOKS[2]):
        response = client.get("/books/5")
    assert response.status_code == 200
    assert response.json()["book_id"] == 5
        
def test_get_book_not_found():
    with patch("routes.books.service.get_book_by_id", side_effect=ValueError("Book 10 not found.")):
        response = client.get("/books/10")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
    
# post routes
def test_add_book():
    with patch("routes.books.service.add_book", return_value=FAKE_BOOKS[0]):
        response = client.post("/books/", json={
            "title": "Don Quixote",
            "author": "Miguel de Cervantes"
        }) # json: the request body
    assert response.status_code == 200
    assert response.json()["title"] == "Don Quixote"
    
def test_add_book_missing_field():
    # patch not needed in this case. pydantic rejects before reaching the service class
    response = client.post("/books/", json={
        "book_id": 7
    })
    assert response.status_code == 422
    
# users routes
def test_get_all_users():
    with patch("routes.users.service.get_all_users", return_value=FAKE_USERS):
        response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Amy"

def test_get_user_found():
    with patch("routes.users.service.get_user_by_id", return_value=FAKE_USERS[1]):
        response = client.get("/users/3")
    assert response.status_code == 200
    assert response.json()["name"] == "Carey"
        
def test_get_user_not_found():
    with patch("routes.users.service.get_user_by_id", side_effect=ValueError("User 4 not found.")):
        response = client.get("/users/4")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
        
def test_get_user_borrowings():
    with patch("routes.users.service.get_user_borrowings", return_value=FAKE_USERS[1].borrowed_books):
        response = client.get("/users/3/borrowings/")
    assert response.status_code == 200
    assert response.json()[0]["book_id"] == 3

# borrowings routes
def test_borrow_book_success():
    mock_result = {"message": "Book borrowed.", "due_date": "Sun Mar 29 2026"}
    with patch("routes.borrowings.service.borrow_book", return_value=mock_result):
        response = client.post("/borrowings/?user_id=1&book_id=3")

    assert response.status_code == 200
    assert response.json()["message"] == "Book borrowed."
    assert response.json()["due_date"] == "Sun Mar 29 2026"
    
def test_borrow_book_already_borrowed():
    with patch("routes.borrowings.service.borrow_book", side_effect=ValueError("Book is already borrowed.")):
        response = client.post("/borrowings/?user_id=1&book_id=3")
    assert response.status_code == 400
    assert "already borrowed" in response.json()["detail"]
    
def test_borrow_book_limit_reached():
    with patch("routes.borrowings.service.borrow_book", side_effect=ValueError("Borrowing limit reached for user")):
        response = client.post("/borrowings/?user_id=1&book_id=3")
    assert response.status_code == 400
    assert "limit reached" in response.json()["detail"]

def test_return_book_success():
    mock_result = {"message": "Book returned."}
    with patch("routes.borrowings.service.return_book", return_value=mock_result):
        response = client.delete("borrowings/?user_id=1&book_id=3")
    
    assert response.status_code == 200
    assert "Book returned." in response.json()["message"]
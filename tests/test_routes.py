from models.book import Book
from models.user import User
from models.borrowing import Borrowing

# books routes
# get routes
def test_get_all_books(client, session):
    session.add(Book(book_id=1, title="Don Quixote",author="Miguel de Cervantes"))
    session.commit()

    response = client.get("/books/")
    
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Don Quixote"

def test_get_book_found(client, session):
    session.add(Book(book_id=5, title="Treasure Island"))
    session.commit()

    response = client.get("/books/5")
    assert response.status_code == 200
    assert response.json()["book_id"] == 5
        
def test_get_book_not_found(client, session):
    response = client.get("/books/10")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
    
# post routes
def test_add_book(client, session):
    response = client.post("/books/", json={
                "title": "Don Quixote",
                "author": "Miguel de Cervantes"
            }) # json: the request body
    assert response.status_code == 200
    assert response.json()["title"] == "Don Quixote"
    
def test_add_book_missing_field(client):
    # patch not needed in this case. pydantic rejects before reaching the service class
    response = client.post("/books/", json={"author": "no title"})

    assert response.status_code == 422

def test_delete_book(client, session):
    session.add(Book(book_id=7, title="To Delete"))
    session.commit()

    response = client.delete("/books/7")
    assert response.status_code == 200
    assert client.get("/books/7").status_code == 404
    
# users routes
def test_get_all_users(client, session):
    session.add(User(user_id=1, name="Arjun"))
    session.commit()
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Arjun"

def test_get_user_found(client, session):
    session.add(User(user_id=1, name="Carey"))
    session.commit()
    
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Carey"
        
def test_get_user_not_found(client):
    response = client.get("/users/4")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_add_user(client):
    response = client.post("/users/", json={"name": "new user"})
    assert response.status_code == 200
    assert response.json()["name"] == "new user"

def test_delete_user(client, session):
    session.add(User(user_id=8, name="to delete"))
    session.commit()
    response = client.delete("/users/8")
    assert response.status_code == 200
    assert client.get("/users/9").status_code == 404
        
def test_get_user_borrowings(client, session):
    session.add_all([
        User(user_id=3, name="Carey"),
        Book(book_id=3, title="The Adventures of Huckleberry Finn"),
        Borrowing(book_id=3, user_id=3, due_date="Sat Oct 24 2026"),
    ])
    session.commit()
    
    response = client.get("/users/3/borrowings/")
    assert response.status_code == 200
    assert response.json()[0]["book_id"] == 3

# borrowings routes
def test_borrow_book_success(client, session):
    session.add_all([
        User(user_id=1, name="Arjun"),
        Book(book_id=3, title="Treasure Island", is_available=True),
    ])
    session.commit()
    response = client.post("/borrowings/?user_id=1&book_id=3")

    assert response.status_code == 200
    assert response.json()["message"] == "Book borrowed."
    
def test_borrow_book_already_borrowed(client, session):
    session.add_all([
        User(user_id=1, name="Arjun"),
        Book(book_id=4, title="Tom Sawyer", is_available=False)
    ])
    session.commit()
    response = client.post("/borrowings/?user_id=1&book_id=4")
    assert response.status_code == 400
    assert "already borrowed" in response.json()["detail"]
    
def test_borrow_book_limit_reached(client, session):
    session.add_all([
        User(user_id=3, name="Carey"),
        Book(book_id=1, title="Don Quixote", is_available=True),
        Book(book_id=4, title="Tom Sawyer", is_available=False),
        Book(book_id=5, title="Treasure Island", is_available=False),
        Borrowing(book_id=4, user_id=3, due_date="Sun Oct 25 2026"),
        Borrowing(book_id=5, user_id=3, due_date="Sun Oct 25 2026"),
    ])
    session.commit()

    response = client.post("/borrowings/?user_id=3&book_id=1")
    assert response.status_code == 400
    assert "limit reached" in response.json()["detail"]

def test_return_book_success(client, session):
    session.add_all([
        User(user_id=1, name="Amy"),
        Book(book_id=3, title="Treasure Island", is_available=False, due_date="Sat Mar 21 2026"),
        Borrowing(book_id=3, user_id=1, due_date="Sat Mar 21 2026"),
    ])
    session.commit()
    
    response = client.delete("borrowings/?user_id=1&book_id=3")
    
    assert response.status_code == 200
    assert "Book returned." in response.json()["message"]
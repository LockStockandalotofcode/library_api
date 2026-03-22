from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "Library API - Visit" in response.json()["message"]

def test_books_router_is_registered():
    response = client.get("/books/")
    assert response.status_code != 404
    
def test_users_router_is_registered():
    response = client.get("/users")
    assert response.status_code != 404

def test_borrowings_router_is_registered():
    response = client.get("/borrowings")
    assert response.status_code != 404
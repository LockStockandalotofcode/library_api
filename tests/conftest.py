import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from database import get_session

from models.book import Book
from models.borrowing import Borrowing
from models.user import User

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:",
             connect_args={"check_same_thread":False},
             poolclass=StaticPool) 
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    "provides a testclient that overrides the real database"
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()
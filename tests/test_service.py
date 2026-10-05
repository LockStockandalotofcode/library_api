import pytest
from services.library_service import LibraryService
from models.book import Book
from models.user import User
from models.borrowing import Borrowing


# FIXTURE for mocking repos
@pytest.fixture
def service(session):
    return LibraryService(session)

def seed_books(session):
    books = [
        Book(book_id=1, title="Don Quixote", author="Miguel de Cervantes", is_available=True),
        Book(book_id=4, title="The Adventures of Tom Sawyer", author="Mark Twain", is_available=False, due_date="Sun Oct 25, 2026"),
        Book(book_id=5, title="Treasure Island", author="Robert Stevenson", is_available=True),
    ]
    session.add_all(books)
    session.commit()

def seed_users(session):
    session.add_all([
        User(user_id=1, name="Arjun"),
        User(user_id=3, name="Ben"),
        ])
    session.commit()

# TESTS for service class
# for books
def test_get_all_books(service, session):
    seed_books(session)
    # call service method
    result = service.get_all_books()
    # assert result
    assert len(result) == 3
    assert result[0].title == "Don Quixote"

def test_get_book_by_id(service, session):
    seed_books(session)
    result = service.get_book_by_id(1)
    assert result.book_id == 1
    assert result.author == "Miguel de Cervantes"

def test_get_book_by_id_not_found(service):
    with pytest.raises(ValueError, match="not found"):
        service.get_book_by_id(99)

# for users
def test_get_all_users(service, session):
    seed_users(session)
    result = service.get_all_users()
    assert len(result) == 2
    assert result[1].name == "Ben"

def test_get_user_by_id(service, session):
    seed_users(session)
    result = service.get_user_by_id(1)
    assert result.user_id == 1
    assert result.name == "Arjun"

def test_get_user_by_id_not_found(service):
    with pytest.raises(ValueError, match="not found"):
        service.get_user_by_id(88)


# for borrowings
def test_get_user_borrowings(service, session):
    seed_books(session)
    seed_users(session)
    session.add_all([
        Borrowing(book_id=4, user_id=3, due_date="Sun Oct 25, 2026"),
        Borrowing(book_id=5, user_id=3, due_date="Sun Oct 25, 2026"),
    ])
    session.commit()
    
    result = service.get_user_borrowings(3)
    assert len(result) == 2
    assert {b.book_id for b in result} == {4, 5}

def test_borrow_book_success(service, session):
    seed_books(session)
    seed_users(session)

    result = service.borrow_book(user_id=1, book_id=5)

    assert result["message"] == "Book borrowed."
    assert "due_date" in result
    assert service.get_book_by_id(5).is_available is False

def test_borrow_book_already_borrowed(service, session):
    seed_books(session)
    seed_users(session)

    with pytest.raises(ValueError, match="Book is already borrowed."):
        service.borrow_book(user_id=1, book_id=4)

def test_borrow_book_limit_reached(service, session):
    seed_books(session)
    seed_users(session)
    session.add_all([
        Borrowing(book_id=4, user_id=3, due_date="Sun Oct 25, 2026"),
        Borrowing(book_id=5, user_id=3, due_date="Sun Oct 25, 2026"),
    ])
    session.commit()

    with pytest.raises(ValueError, match="Borrowing limit reached for user 3."):
        service.borrow_book(user_id=3, book_id=1)

def test_return_book(service, session):
    seed_books(session)
    seed_users(session)
    session.add_all([
        Borrowing(book_id=4, user_id=3, due_date="Sun Oct 25, 2026"),
    ])
    session.commit()

    result = service.return_book(user_id=3, book_id=4)

    assert result["message"] == "Book returned."
    book = service.get_book_by_id(4)
    assert book.is_available is True
    assert book.due_date is None

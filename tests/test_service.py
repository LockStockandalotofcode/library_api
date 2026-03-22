import pytest
from unittest.mock import MagicMock
from services.library_service import LibraryService
from models.book import Book
from models.user import User

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
# FIXTURE for mocking repos
@pytest.fixture
def service():
    s = LibraryService()
    s.book_repo = MagicMock()
    s.user_repo = MagicMock()
    return s

# TESTS for service class
# for books
def test_get_all_books(service):
    # set return value for methods needed
    service.book_repo.load_books.return_value = FAKE_BOOKS
    # call service method
    result = service.get_all_books()
    # assert result
    assert len(result) == 3
    assert result[0].title == "Don Quixote"

def test_get_book_by_id(service):
    service.book_repo.find_book_by_id.return_value = FAKE_BOOKS[0]
    
    result = service.get_book_by_id(1)
    assert result.book_id == 1
    assert result.author == "Miguel de Cervantes"

# for users
def test_get_all_users(service):
    service.user_repo.load_users.return_value = FAKE_USERS
    result = service.get_all_users()
    assert len(result) == 2
    assert result[1].name == "Carey"

def test_get_user_by_id(service):
    service.user_repo.find_user_by_id.return_value = FAKE_USERS[1]
    result = service.get_user_by_id(4)
    assert result.user_id == 3
    assert result.name == "Carey"

# for borrowings
def test_get_user_borrowings(service):
    service.user_repo.find_user_by_id.return_value = FAKE_USERS[1]
    result = service.get_user_borrowings(3)
    assert len(result) == 2
    assert result[1].book_id == 4
    assert result[0].book_id == 3

def test_borrow_book_success(service):
    service.book_repo.find_book_by_id.return_value = FAKE_BOOKS[2]
    service.user_repo.find_user_by_id.return_value = FAKE_USERS[0]

    result = service.borrow_book(user_id=1, book_id=5)

    assert result["message"] == "Book borrowed."
    assert "due_date" in result
    service.book_repo.save_books.assert_called_once()
    service.user_repo.save_users.assert_called_once()
    
def test_borrow_book_already_borrowed(service):
    service.book_repo.find_book_by_id.return_value = FAKE_BOOKS[1]
    service.user_repo.find_user_by_id.return_value = FAKE_USERS[0]

    with pytest.raises(ValueError, match="Book is already borrowed."):
        service.borrow_book(user_id=1, book_id=4)

def test_borrow_book_limit_reached(service):
    service.book_repo.find_book_by_id.return_value = FAKE_BOOKS[0]
    service.user_repo.find_user_by_id.return_value = FAKE_USERS[1]

    with pytest.raises(ValueError, match="Borrowing limit reached for user 3."):
        service.borrow_book(user_id=4, book_id=1)

def test_return_book(service):
    service.book_repo.find_book_by_id.return_value = FAKE_BOOKS[1]
    service.user_repo.find_user_by_id.return_value = FAKE_USERS[1]

    result = service.return_book(user_id=3, book_id=4)

    assert result["message"] == "Book returned."
    service.book_repo.save_books.assert_called_once()
    service.user_repo.save_users.assert_called_once()

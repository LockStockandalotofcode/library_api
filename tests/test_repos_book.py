import pytest
import json
from unittest.mock import patch, mock_open
from repositories.book_repo import BookRepository
from models.book import Book

@pytest.fixture
def fake_books_json(): # JSON data for mocking
    return json.dumps([
        {"book_id": 1, "title": "Don Quixote",  "author": "Miguel de Cervantes", "is_available": True,  "due_date": None},

        {"book_id": 2, "title": "Moby Dick",    "author": "Herman Melville", "is_available": False, "due_date": "Mon Mar 23 2025"},
        ])

@pytest.fixture
def fake_books_py(): # python Book objects
    return [
        Book(book_id=1, title="Don Quixote",  author="Miguel de Cervantes", is_available=True,  due_date=None),

        Book(book_id=2, title="Moby Dick",    author="Herman Melville", is_available=False, due_date="Mon Mar 23 2025"),
    ]

repo = BookRepository()

# LOAD
def test_load_books(fake_books_json):
    with patch("builtins.open", mock_open(read_data=fake_books_json)):
        books = repo.load_books()
    assert len(books) == 2
    assert isinstance(books[0], Book)
    assert books[1].is_available == False
    assert books[0].title == "Don Quixote"

# SAVE
# all std files open() and json file are patched
def test_save_books_correctly_converts_to_json(fake_books_py):
    with patch("builtins.open", mock_open()) as mocked_file, patch("json.dump") as mocked_json_dump:
        # act
        repo.save_books(fake_books_py)

        # Assert
        # check if it was called at least once
        assert mocked_json_dump.called
        # inspect arguments
        written_books = mocked_json_dump.call_args[0][0] #gets first positional argument # the json data passed to the function
        # it being the first of positional args
        # call_args attribute returns a tuple of args, kwargs
        assert len(written_books) == 2
        assert isinstance(written_books[0], dict)
        # check arguments individually
        assert written_books[0]["title"] == "Don Quixote"
        assert written_books[1]["is_available"] == False

def test_find_book_by_id(fake_books_json):
    with patch("builtins.open", mock_open(read_data=fake_books_json)):
        # act
        book = repo.find_book_by_id(book_id=2)

        # assert
        assert book is not None
        assert book.book_id == 2
        assert book.title == "Moby Dick"
import pytest
from models.book import Book, BookCreate
from pydantic import ValidationError

def test_model_book():
    book = Book(book_id=1, title="Don Quixote", author="Miguel de Cervantes")
    assert book.title == "Don Quixote"

def test_model_book_rejects_bad_data():
    with pytest.raises(ValidationError):
        BookCreate.model_validate({"author":"Don Quixote"})
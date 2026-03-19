import pytest
from models.book import Book

def test_model_book():
    book = Book(book_id=1, title="Don Quixote", author="Miguel de Cervantes")
    assert book.title == "Don Quixote"

def test_model_book_rejects_bad_data():
    with pytest.raises(Exception):
        Book(book_id="four", title="Don Quixote")
    
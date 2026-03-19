import pytest
from models.book import Book

def test_model_book():
    book = Book(book_id=1, title="Don Quixote", author="Miguel de Cervantes")
    assert book.title == "Don Quixote"
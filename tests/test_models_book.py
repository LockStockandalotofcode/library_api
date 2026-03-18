import pytest
from models.book import Book

def test_book_model():
    book = Book(id=1, title="Don Quixote", author="Miguel de Cervantes")
    assert book.title == "Don Quixote"
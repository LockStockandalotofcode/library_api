from repositories.book_repo import BookRepository
from models.book import Book

def test_load_books(session):
    session.add_all([
        Book(book_id=1, title="Don Quixote", author="Miguel de Cervantes", is_available=True),
        Book(book_id=2, title="Moby Dick", author="Herman Melville", is_available=False, due_date="Mon Oct 26 2025"),
    ])
    session.commit()

    books = BookRepository(session).load()

    assert len(books) == 2
    assert isinstance(books[0], Book)
    assert books[1].is_available is False
    assert books[0].title == "Don Quixote"

def test_find_book_by_id(session):
    session.add(Book(book_id=2, title="Moby Dick", author="Herman Melville"))
    session.commit()

    book = BookRepository(session).find_book_by_id(2)
    assert book is not None
    assert book.title == "Moby Dick"

def test_find_book_by_id_missing(session):
    assert BookRepository(session).find_book_by_id(90) is None

def test_save_book_assigns_id(session):
    saved = BookRepository(session).save(Book(title="Book 5", author="me"))
    assert saved.book_id is not None

def test_delete_book(session):
    session.add(Book(book_id=3, title="To be deleted"))
    session.commit()
    repo = BookRepository(session)
    repo.delete(repo.find_book_by_id(3))
    assert repo.find_book_by_id(3) is None
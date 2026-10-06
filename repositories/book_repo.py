from sqlmodel import Session, select
from models.book import Book, BookCreate

class BookRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def load(self) -> list[Book]:
        return self.session.exec(select(Book)).all()

    def find_book_by_id(self, book_id: int) -> Book | None:
        return self.session.get(Book, book_id)

    def save(self, book_data:BookCreate) -> Book:
        if isinstance(book_data, Book):
            db_book = book_data
        else:
            db_book = Book.model_validate(book_data)
        self.session.add(db_book)
        self.session.commit()
        self.session.refresh(db_book)
        return db_book

    def delete(self, book: Book) -> None:
        self.session.delete(book)
        self.session.commit()

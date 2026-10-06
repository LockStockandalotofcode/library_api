from sqlmodel import Session, select
from models.book import Book, BookCreate

class BookRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def load(self) -> list[Book]:
        return self.session.exec(select(Book)).all()

    def find_book_by_id(self, book_id: int) -> Book | None:
        return self.session.get(Book, book_id)

    def save(self, book:BookCreate) -> Book:
        db_book = Book.model_validate(book)
        self.session.add(db_book)
        self.session.commit()
        self.session.refresh(db_book)
        return db_book

    def delete(self, book: Book) -> None:
        self.session.delete(book)
        self.session.commit()

from sqlmodel import Session, select
from models.book import Book

class BookRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def load(self) -> list[Book]:
        return self.session.exec(select(Book)).all()

    def find_book_by_id(self, book_id: int) -> Book | None:
        return self.session.get(Book, book_id)

    def save(self, book:Book) -> Book:
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.session.delete(book)
        self.session.commit()

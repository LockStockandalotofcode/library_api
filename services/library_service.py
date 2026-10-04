from datetime import datetime, timedelta
from sqlmodel import Session, select
from repositories.book_repo import BookRepository
from repositories.user_repo import UserRepository
from models.book import Book
from models.user import User
from models.borrowing import Borrowing

class LibraryService:
    def __init__(self, session:Session):
        self.session = session
        self.book_repo = BookRepository(session)
        self.user_repo = UserRepository(session)

    # BOOKS
    def get_all_books(self) -> list[Book]:
        return self.book_repo.load()

    def get_book_by_id(self, book_id: int) -> Book:
        book = self.book_repo.find_book_by_id(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found.")
        return book

    def add_book(self, book_data: dict) -> Book:
        return self.book_repo.save(Book(**book_data))

    def remove_book(self, book_id: int) -> dict:
        book = self.get_book_by_id(book_id)
        self.book_repo.delete(book)
        return {"message": f"Book {book_id} removed."}

    # USERS
    def get_all_users(self) -> list[User]:
        return self.user_repo.load()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.find_user_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found.")
        return user

    def add_user(self, user_data: dict) -> User:
        return self.user_repo.save(User(**user_data))

    def remove_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.user_repo.delete(user)
        return {"message": f"User {user_id} removed."}

    def get_user_borrowings(self, user_id: int) -> list[Borrowing]:
        # to validate user existence, in which case an empty list is not returned, instead execution stops as an exception or error is raised
        self.get_user_by_id(user_id)
        return self.session.exec(
            select(Borrowing).where(Borrowing.user_id == user_id)
        ).all()

    # BORROWINGS
    def borrow_book(self, user_id: int, book_id: int) -> dict:
        # validate request
        user = self.get_user_by_id(user_id)
        book = self.get_book_by_id(book_id)

        # CONSTRAINTS
        if not book.is_available:
            raise ValueError("Book is already borrowed.")
        if len(self.get_user_borrowings(user_id)) >= 2:
            raise ValueError(f"Borrowing limit reached for user {user.user_id}.")
        
        # APPLY changes to system
        due_date = (datetime.now() + timedelta(days=7)).strftime("%a %b %d %Y")
        book.is_available = False
        book.due_date = due_date
        self.book_repo.save(book)

        self.session.add(Borrowing(book_id=book.book_id, user_id=user.user_id, due_date=due_date))
        self.session.commit()

        return {"message": "Book borrowed.", "due_date": due_date, "user": user}

    def return_book(self, user_id: int, book_id: int) -> dict:
        book = self.get_book_by_id(book_id)
        book.is_available = True
        book.due_date = None
        self.book_repo.save(book)
        
        borrowing = self.session.exec(
            select(Borrowing).where(Borrowing.user_id == user_id, Borrowing.book_id == book_id)
        ).first()
        if borrowing:
            self.session.delete(borrowing)
            self.session.commit()

        return {"message": "Book returned."}

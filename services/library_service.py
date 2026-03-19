from datetime import datetime, timedelta
from repositories.book_repo import BookRepository
from repositories.user_repo import UserRepository
from models.book import Book
from models.user import User

class LibraryService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.user_repo = UserRepository()

    # BOOKS
    def get_all_books()

    def get_book_by_id()

    def add_book()

    def remove_book()

    # USERS

    def get_all_users()

    def get_user_by_id()

    def get_user_borrowings()

    # BORROWINGS
    def borrow_book()

    def return_book()
    
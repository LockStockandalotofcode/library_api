from models.user import User, UserCreate
from sqlmodel import Session, select

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def load(self) -> list[User]:
        return self.session.exec(select(User)).all()
    
    def find_user_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def save(self, user: UserCreate) -> User:
        db_user = User.model_validate(user)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
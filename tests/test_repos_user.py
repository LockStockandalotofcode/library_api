from repositories.user_repo import UserRepository
from models.user import User

def test_load_users(session):
    session.add_all([
        User(user_id=1, name="Arjun"),
        User(user_id=3, name="Carey"),
    ])
    session.commit()

    users = UserRepository(session).load()
    assert len(users) == 2
    assert users[1].name == "Carey"

def test_find_user_by_id(session):
    session.add(User(user_id=3, name="Carey"))
    session.commit()

    user = UserRepository(session).find_user_by_id(3)
    assert user is not None
    assert user.name == "Carey"
    
def test_find_user_by_id_missing(session):
    assert UserRepository(session).find_user_by_id(80) is None

def test_save_user_assigns_id(session):
    saved = UserRepository(session).save(User(name="New User"))
    assert saved.user_id is not None

def test_delete_user(session):
    session.add(User(user_id=7, name="to delete"))
    session.commit()
    repo = UserRepository(session)

    repo.delete(repo.find_user_by_id(7))
    assert repo.find_user_by_id(7) is None
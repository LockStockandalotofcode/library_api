import pytest
from models.user import User

def test_model_user():
    user = User(user_id= 1, name="Amy")
    assert user.name == "Amy"
import pytest
from models.user import User

def test_model_user():
    user = User(user_id= 1, name="Amy")
    assert user.name == "Amy"

def test_model_user_rejects_bad_data():
    with pytest.raises(Exception):
        User(user_id="4", name=3)
        # here string is handled by pydantic but name as int is not converted to string
    
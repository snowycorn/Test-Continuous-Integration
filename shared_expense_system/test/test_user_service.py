import pytest

from models.user import User
from services.user_service import UserService

@pytest.fixture
def sample_data():
    return {"users": {"Alice": User("Alice"), "Bob": User("Bob")}, "groups": []}

def test_add_user(sample_data):
    sample_data["users"]["Charlie"] = User("Charlie")
    assert "Charlie" in sample_data["users"]

def test_delete_user(sample_data):
    del sample_data["users"]["Alice"]
    assert "Alice" not in sample_data["users"]

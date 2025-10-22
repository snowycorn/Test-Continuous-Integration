import pytest

from models.user import User
from models.group import Group
from services.group_service import GroupService

@pytest.fixture
def sample_data():
    users = {"Alice": User("Alice"), "Bob": User("Bob")}
    groups = [Group("Trip"), Group("Work")]
    return {"users": users, "groups": groups}

def test_add_group(sample_data):
    new_group = Group("Party")
    sample_data["groups"].append(new_group)
    assert any(g.name == "Party" for g in sample_data["groups"])

def test_add_user_to_group(sample_data):
    group = sample_data["groups"][0]
    user = sample_data["users"]["Alice"]
    group.members.append(user)
    assert user in group.members

def test_remove_user_from_group(sample_data):
    group = sample_data["groups"][0]
    user = sample_data["users"]["Bob"]
    group.members.append(user)
    group.members.remove(user)
    assert user not in group.members

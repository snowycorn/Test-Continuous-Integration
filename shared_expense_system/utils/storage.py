import json
from models.user import User
from models.group import Group

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            raw = json.load(f)
        users = {name: User.from_dict(u) for name, u in raw.get("users", {}).items()}
        groups = [Group.from_dict(g, users) for g in raw.get("groups", [])]
        return {"users": users, "groups": groups}
    except FileNotFoundError:
        return {"users": {}, "groups": []}

def save_data(data):
    users_dict = {name: u.to_dict() for name, u in data["users"].items()}
    groups_list = [g.to_dict() for g in data["groups"]]
    with open(DATA_FILE, "w") as f:
        json.dump({"users": users_dict, "groups": groups_list}, f, indent=4)

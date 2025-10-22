class User:
    def __init__(self, name):
        self.name = name
        self.balance = 0  # 正數表示應收，負數表示應付

    def to_dict(self):
        return {"name": self.name, "balance": self.balance}

    @staticmethod
    def from_dict(d):
        u = User(d["name"])
        u.balance = d["balance"]
        return u

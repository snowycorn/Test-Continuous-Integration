class Group:
    def __init__(self, name):
        self.name = name
        self.members = []      # list of User
        self.expenses = []     # list of Expense

    def to_dict(self):
        return {
            "name": self.name,
            "members": [m.name for m in self.members],
            "expenses": [e.to_dict() for e in self.expenses]
        }

    @staticmethod
    def from_dict(d, users_dict):
        g = Group(d["name"])
        g.members = [users_dict[name] for name in d["members"] if name in users_dict]
        from models.expense import Expense
        g.expenses = [Expense.from_dict(e, users_dict) for e in d["expenses"]]
        return g

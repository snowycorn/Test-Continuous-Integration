class Expense:
    def __init__(self, payer, amount, participants, category="Other", note=""):
        self.payer = payer         # User
        self.amount = amount
        self.participants = participants  # list of User
        self.category = category
        self.note = note

    def to_dict(self):
        return {
            "payer": self.payer.name,
            "amount": self.amount,
            "participants": [p.name for p in self.participants],
            "category": self.category,
            "note": self.note
        }

    @staticmethod
    def from_dict(d, users_dict):
        payer = users_dict[d["payer"]]
        participants = [users_dict[name] for name in d["participants"]]
        return Expense(payer, d["amount"], participants, d["category"], d["note"])

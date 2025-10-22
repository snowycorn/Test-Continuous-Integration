from models.expense import Expense
from utils.calculation import split_amount

class ExpenseService:
    def __init__(self, data):
        self.data = data

    def menu(self):
        print("\n--- Expense Management ---")
        print("1. Add Expense")
        print("2. Delete Expense")
        choice = input("Select: ")

        if choice == "1":
            self.add_expense_ui()
        elif choice == "2":
            self.delete_expense_ui()

    def add_expense_ui(self):
        groups = self.data["groups"]
        if not groups:
            print("No groups available.")
            return
        print("Groups:")
        for i, g in enumerate(groups, 1):
            print(f"{i}. {g.name}")
        g_idx = int(input("Select group number: ")) - 1
        if g_idx < 0 or g_idx >= len(groups):
            print("Invalid selection.")
            return
        group = groups[g_idx]

        if not group.members:
            print("No members in group.")
            return
        print("Members:")
        for i, u in enumerate(group.members, 1):
            print(f"{i}. {u.name}")
        payer_idx = int(input("Select payer number: ")) - 1
        if payer_idx < 0 or payer_idx >= len(group.members):
            print("Invalid selection.")
            return
        payer = group.members[payer_idx]

        print("Select participants (comma separated numbers, e.g., 1,2):")
        for i, u in enumerate(group.members, 1):
            print(f"{i}. {u.name}")
        part_input = input("Participants: ")
        part_indices = [int(x.strip())-1 for x in part_input.split(",")]
        participants = [group.members[i] for i in part_indices if 0 <= i < len(group.members)]

        amount = float(input("Amount: "))
        category = input("Category [Food/Travel/Utilities/Other]: ") or "Other"
        note = input("Note: ")

        shares = split_amount(amount, participants)
        for u, share in zip(participants, shares):
            u.balance -= share
        payer.balance += amount

        group.expenses.append(Expense(payer, amount, participants, category, note))
        print("Expense added.")

    def delete_expense_ui(self):
        groups = self.data["groups"]
        if not groups:
            print("No groups.")
            return
        print("Groups:")
        for i, g in enumerate(groups, 1):
            print(f"{i}. {g.name}")
        g_idx = int(input("Select group number: ")) - 1
        group = groups[g_idx]

        if not group.expenses:
            print("No expenses to delete.")
            return
        print("Expenses:")
        for i, e in enumerate(group.expenses, 1):
            print(f"{i}. {e.payer.name} paid {e.amount} ({e.category}) - {e.note}")
        e_idx = int(input("Select expense number to delete: ")) - 1
        exp = group.expenses.pop(e_idx)
        shares = split_amount(exp.amount, exp.participants)
        for u, share in zip(exp.participants, shares):
            u.balance += share
        exp.payer.balance -= exp.amount
        print("Expense deleted.")

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
        group = self.select_group()
        if group is None:
            return
        payer = self.select_member(group)
        if payer is None:
            return
        participants = self.select_participants(group)
        if participants is None:
            return
        amount = float(input("Amount: "))
        category = input("Category [Food/Travel/Utilities/Other]: ") or "Other"
        note = input("Note: ")
        self.add_expense(group, payer, participants, amount, category, note)
        print("Expense added.")

    def delete_expense_ui(self):
        group = self.select_group()
        if group is None:
            return
        expense_id = self.select_expense(group)
        if expense_id is None:
            return
        self.delete_expense(group, expense_id)
        print("Expense deleted.")

    def select_group(self):
        groups = self.data["groups"]
        if not groups:
            print("No groups available.")
            return None
        
        # list all group
        print("Groups:")
        for i, g in enumerate(groups, 1):
            print(f"{i}. {g.name}")
        
        # user input
        g_idx = int(input("Select group number: ")) - 1
        if g_idx < 0 or g_idx >= len(groups):
            print("Invalid selection.")
            return None
        
        return groups[g_idx]        
    
    def select_member(self, group):
        if not group.members:
            print("No members in group.")
            return None
        
        # list all members in the group
        print("Members:")
        for i, u in enumerate(group.members, 1):
            print(f"{i}. {u.name}")

        # user input
        payer_idx = int(input("Select payer number: ")) - 1
        if payer_idx < 0 or payer_idx >= len(group.members):
            print("Invalid selection.")
            return None
        
        return group.members[payer_idx]
    
    def select_participants(self, group):
        # list all members in the group
        print("Select participants (comma separated numbers, e.g., 1,2):")
        for i, u in enumerate(group.members, 1):
            print(f"{i}. {u.name}")
        
        # user input
        part_input = input("Participants: ")
        part_indices = [int(x.strip())-1 for x in part_input.split(",")]
        participants = [group.members[i] for i in part_indices if 0 <= i < len(group.members)]
        if len(participants) == 0:
            return None
            
        return participants
    
    def select_expense(self, group):
        if not group.expenses:
            print("No expenses to delete.")
            return
        print("Expenses:")
        for i, e in enumerate(group.expenses, 1):
            print(f"{i}. {e.payer.name} paid {e.amount} ({e.category}) - {e.note}")
        index = int(input("Select expense number to delete: ")) - 1
        
        # check if the input index is valid
        if index < 0 or index >= len(group.expenses):
            print("Invalid selection.")
            return None
        else:
            return index

    def delete_expense(self, group, expense_id):
        """Core logic: handles only computation and data update"""
        expense = group.expenses.pop(expense_id)
        shares = split_amount(expense.amount, expense.participants)
        for u, share in zip(expense.participants, shares):
            u.balance += share
        expense.payer.balance -= expense.amount
        return
        

    def add_expense(self, group, payer, participants, amount, category, note):
        """Core logic: handles only computation and data update"""
        shares = split_amount(amount, participants)
        for u, share in zip(participants, shares):
            u.balance -= share
        payer.balance += amount
        group.expenses.append(Expense(payer, amount, participants, category, note))
        return

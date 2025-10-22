class ReportService:
    def __init__(self, data):
        self.data = data

    def menu(self):
        groups = self.data["groups"]
        if not groups:
            print("No groups.")
            return
        print("Groups:")
        for i, g in enumerate(groups, 1):
            print(f"{i}. {g.name}")
        g_idx = int(input("Select group number: ")) - 1
        group = groups[g_idx]

        self.print_report(group)

    def print_report(self, group):
        print(f"\nReport for group: {group.name}")
        total = sum(e.amount for e in group.expenses)
        print(f"Total spent: {total:.2f}")
        print("Individual balances:")
        for m in group.members:
            print(f"{m.name}: {m.balance:.2f}")

        print("\nSuggested payments:")
        debtors = [m for m in group.members if m.balance < 0]
        creditors = [m for m in group.members if m.balance > 0]
        for d in debtors:
            for c in creditors:
                pay = min(-d.balance, c.balance)
                if pay > 0:
                    print(f"{d.name} pays {c.name}: {pay:.2f}")
                    d.balance += pay
                    c.balance -= pay

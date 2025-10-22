from services.user_service import UserService
from services.group_service import GroupService
from services.expense_service import ExpenseService
from services.report_service import ReportService
from utils.storage import load_data, save_data

def main():
    data = load_data()
    user_service = UserService(data)
    group_service = GroupService(data)
    expense_service = ExpenseService(data)
    report_service = ReportService(data)

    while True:
        print("\n--- Shared Expense System ---")
        print("1. User Management")
        print("2. Group Management")
        print("3. Expense Management")
        print("4. Report")
        print("0. Exit")
        choice = input("Select option: ")

        if choice == "1":
            user_service.menu()
        elif choice == "2":
            group_service.menu()
        elif choice == "3":
            expense_service.menu()
        elif choice == "4":
            report_service.menu()
        elif choice == "0":
            save_data(data)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
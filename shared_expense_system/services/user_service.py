from models.user import User

class UserService:
    def __init__(self, data):
        self.data = data  # {"users": {...}, "groups": [...]}

    def menu(self):
        while True:
            print("\n--- User Management ---")
            self.list_users(show_header=False)

            print("\nOptions:")
            print("1. Add User")
            print("2. Delete User")
            print("0. Return to Main Menu")

            choice = input("Select: ").strip()
            if choice == "1":
                self.add_user()
            elif choice == "2":
                self.delete_user()
            elif choice == "0":
                break
            else:
                print("Invalid option.")

    # ========== 新增使用者 ==========
    def add_user(self):
        name = input("Enter new user name: ").strip()
        if not name:
            print("User name cannot be empty.")
            return
        if name in self.data["users"]:
            print("User already exists.")
            return
        self.data["users"][name] = User(name)
        print(f"✅ User '{name}' added.")

    # ========== 刪除使用者 ==========
    def delete_user(self):
        users = list(self.data["users"].values())
        if not users:
            print("No users to delete.")
            return

        print("\nUsers:")
        for i, u in enumerate(users, 1):
            print(f"{i}. {u.name}")

        idx = input("Select user number to delete (0 to cancel): ").strip()
        if not idx.isdigit() or int(idx) == 0:
            return
        idx = int(idx) - 1
        if idx < 0 or idx >= len(users):
            print("Invalid user number.")
            return

        user = users[idx]
        name = user.name

        # 從群組中移除
        for g in self.data["groups"]:
            g.members = [m for m in g.members if m.name != name]

        del self.data["users"][name]
        print(f"🗑️ User '{name}' deleted (and removed from all groups).")

    # ========== 列出所有使用者 ==========
    def list_users(self, show_header=True):
        if show_header:
            print("\n--- User List ---")
        users = list(self.data["users"].values())
        if not users:
            print("No users found.")
            return
        for i, u in enumerate(users, 1):
            print(f"{i}. {u.name}")

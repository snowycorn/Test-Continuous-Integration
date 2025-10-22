from models.group import Group
from models.user import User

class GroupService:
    def __init__(self, data):
        self.data = data  # {"users": {...}, "groups": [...]}

    def menu(self):
        while True:
            print("\n--- Group Management ---")
            if not self.data["groups"]:
                print("No groups yet.")
            else:
                print("Groups:")
                for i, g in enumerate(self.data["groups"], 1):
                    members = ", ".join(u.name for u in g.members) if g.members else "No members"
                    print(f"{i}. {g.name} ({members})")

            print("\nOptions:")
            print("1. Add Group")
            print("2. Delete Group")
            print("3. Manage Group Members")
            print("0. Return to Main Menu")

            choice = input("Select: ").strip()
            if choice == "1":
                self.add_group()
            elif choice == "2":
                self.delete_group()
            elif choice == "3":
                self.manage_group_members()
            elif choice == "0":
                break
            else:
                print("Invalid option.")

    # ========== 基本操作 ==========
    def add_group(self):
        name = input("Enter new group name: ").strip()
        if any(g.name == name for g in self.data["groups"]):
            print("Group already exists.")
            return
        self.data["groups"].append(Group(name))
        print(f"✅ Group '{name}' added.")

    def delete_group(self):
        if not self.data["groups"]:
            print("No groups to delete.")
            return
        self.list_groups()
        idx = input("Select group number to delete (0 to cancel): ").strip()
        if not idx.isdigit() or int(idx) == 0:
            return
        idx = int(idx) - 1
        if idx < 0 or idx >= len(self.data["groups"]):
            print("Invalid group number.")
            return
        name = self.data["groups"][idx].name
        del self.data["groups"][idx]
        print(f"🗑️ Group '{name}' deleted.")

    # ========== 群組成員管理 ==========
    def manage_group_members(self):
        if not self.data["groups"]:
            print("No groups available.")
            return

        self.list_groups()
        idx = input("Select group number (0 to return): ").strip()
        if not idx.isdigit() or int(idx) == 0:
            return
        idx = int(idx) - 1
        if idx < 0 or idx >= len(self.data["groups"]):
            print("Invalid group number.")
            return

        group = self.data["groups"][idx]
        while True:
            print(f"\n--- Manage Group: {group.name} ---")
            members = ", ".join(u.name for u in group.members) if group.members else "No members yet"
            print(f"Members: {members}")

            print("\n1. Add User to Group")
            print("2. Remove User from Group")
            print("0. Back to Group List")

            choice = input("Select: ").strip()
            if choice == "1":
                self.add_user_to_group(group)
            elif choice == "2":
                self.remove_user_from_group(group)
            elif choice == "0":
                break
            else:
                print("Invalid option.")

    # ========== 具體操作 ==========
    def add_user_to_group(self, group):
        available_users = [u for u in self.data["users"].values() if u not in group.members]
        if not available_users:
            print("No available users to add.")
            return
        print("\nAvailable Users:")
        for i, u in enumerate(available_users, 1):
            print(f"{i}. {u.name}")

        idx = input("Select user number to add (0 to cancel): ").strip()
        if not idx.isdigit() or int(idx) == 0:
            return
        idx = int(idx) - 1
        if idx < 0 or idx >= len(available_users):
            print("Invalid user number.")
            return
        user = available_users[idx]
        group.members.append(user)
        print(f"✅ Added '{user.name}' to group '{group.name}'.")

    def remove_user_from_group(self, group):
        if not group.members:
            print("No members in this group.")
            return
        print("\nGroup Members:")
        for i, u in enumerate(group.members, 1):
            print(f"{i}. {u.name}")

        idx = input("Select user number to remove (0 to cancel): ").strip()
        if not idx.isdigit() or int(idx) == 0:
            return
        idx = int(idx) - 1
        if idx < 0 or idx >= len(group.members):
            print("Invalid user number.")
            return
        user = group.members[idx]
        group.members.remove(user)
        print(f"🗑️ Removed '{user.name}' from group '{group.name}'.")

    def list_groups(self):
        print("\nGroups:")
        for i, g in enumerate(self.data["groups"], 1):
            members = ", ".join(u.name for u in g.members) if g.members else "No members"
            print(f"{i}. {g.name} ({members})")

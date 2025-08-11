
import re
import pwinput
from services.user_service import UserService
from services.auth_service import AuthService
from services.expense_service import ExpenseService
from services.group_service import GroupService
from utils.print_service import display_message
from datetime import datetime

class CoreService:

    @staticmethod
    def is_strong_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[@#$%&*!]', password):
            return False
        return True

    @staticmethod
    def run_app():
        while True:
            print("\n=== Money Manager ===")
            choice = input("Enter \n 1 to Register \n 2 to Login \n 0 to Exit: ").strip()

            if choice == "1":
                CoreService.register_flow()
            elif choice == "2":
                CoreService.login_flow()
            elif choice == "0":
                display_message("Thank you for using the app!")
                break
            else:
                display_message("Invalid choice. Please try again.")

    @staticmethod
    def register_flow():
        while True:
            while True:
                username = input("Choose a username: ").strip()
                if not re.match(r'^[A-Za-z0-9_]{4,20}$', username):
                    display_message("Invalid username. Use 4-20 characters (letters, numbers, underscores).")
                    continue
                if UserService.is_username_taken(username):
                    display_message("Username already exists. Please try a different username.")
                    continue
                break

            while True:
                name = input("Enter your full name: ").strip()
                if not name:
                    display_message("Name cannot be empty.")
                else:
                    break

            while True:
                password = pwinput.pwinput("Choose a password: ", mask='*')
                if not CoreService.is_strong_password(password):
                    display_message(
                        "Weak password! Your password must:\n"
                        "- Be at least 8 characters long\n"
                        "- Contain at least one uppercase letter\n"
                        "- Contain at least one lowercase letter\n"
                        "- Contain at least one number\n"
                        "- Contain at least one special character (e.g. @, #, $, %)"
                    )
                else:
                    break

            message = UserService.register_user(username, name, password)
            display_message(message)
            if "successful" in message.lower():
                break

    @staticmethod
    def login_flow():
        while True:
            username = input("Enter username (or '0' to cancel): ").strip()
            if username == "0":
                display_message("Login cancelled. Returning to main menu.")
                return

            password = pwinput.pwinput("Enter password (or '0' to cancel): ", mask='*')
            if password == "0":
                display_message("Login cancelled. Returning to main menu.")
                return

            success, user_id = AuthService.login(username, password)
            if success:
                display_message("Login successful!")
                CoreService.expense_menu(user_id)
                break
            else:
                display_message("Invalid credentials! Please try again.")

    @staticmethod
    def expense_menu(user_id):
        while True:
            print("\n=== Expense Menu ===")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Update Expense")
            print("4. Delete Expense")
            print("5. Group Expense Splitter")
            print("0. Logout")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                ExpenseService.add_expense(user_id)
            elif choice == "2":
                ExpenseService.view_expenses(user_id)
            elif choice == "3":
                ExpenseService.update_expense(user_id)
            elif choice == "4":
                ExpenseService.delete_expense(user_id)
            elif choice == "5":
                CoreService.group_expense_menu(user_id)
            elif choice == "0":
                display_message("Logged out successfully!")
                break
            else:
                display_message("Invalid option. Try again.")

    @staticmethod
    def group_expense_menu(user_id):
        while True:
            print("\n=== Group Expense Menu ===")
            print("1. Create Group")
            print("2. Add Member to Group")
            print("3. List Groups")
            print("4. View Group Members")
            print("5. Add Group Expense")
            print("6. View Group Expenses")
            print("0. Back to Expense Menu")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                group_name = input("Enter group name: ").strip()
                if group_name:
                    GroupService.create_group(group_name, user_id)
                else:
                    display_message("Group name cannot be empty.")

            elif choice == "2":
                groups = GroupService.list_groups(user_id)
                if not groups:
                    continue
                try:
                    group_id = int(input("Enter group ID to add member: "))
                    UserService.list_all_users()
                    member_id = int(input("Enter user ID to add: "))
                    GroupService.add_member_to_group(group_id, member_id)
                except ValueError:
                    display_message("Invalid input. Please enter numeric IDs.")

            elif choice == "3":
                GroupService.list_groups(user_id)

            elif choice == "4":
                groups = GroupService.list_groups(user_id)
                if not groups:
                    continue
                try:
                    group_id = int(input("Enter group ID to view members: "))
                    GroupService.list_group_members(group_id)
                except ValueError:
                    display_message("Invalid group ID.")

            elif choice == "5":
                groups = GroupService.list_groups(user_id)
                if not groups:
                    continue

                try:
                    group_id = int(input("Enter group ID for the expense: "))
                except ValueError:
                    display_message("Invalid group ID. Please enter a number.")
                    continue

                # Loop until valid amount entered
                while True:
                    amount_input = input("Enter total amount: ").strip()
                    try:
                        amount = float(amount_input)
                        if amount <= 0:
                            display_message("Amount must be a positive number.")
                        else:
                            break
                    except ValueError:
                        display_message("Invalid amount. Please enter a numeric value.")

                # Loop until valid non-empty category
                while True:
                    category = input("Enter category: ").strip()
                    if not category:
                        display_message("Category cannot be empty.")
                    else:
                        break

                # Loop until valid non-empty description
                while True:
                    description = input("Enter description: ").strip()
                    if not description:
                        display_message("Description cannot be empty.")
                    else:
                        break

                # Loop until valid date entered
                while True:
                    date = input("Enter date (YYYY-MM-DD): ").strip()
                    if not date:
                        display_message("Date cannot be empty.")
                        continue
                    try:
                        datetime.strptime(date, '%Y-%m-%d')
                        break
                    except ValueError:
                        display_message("Date format invalid. Use YYYY-MM-DD.")

                members = GroupService.list_group_members(group_id)
                if not members:
                    continue

                share_per_member = round(amount / len(members), 2)
                print("\nEach member will pay (equal split):")
                for member in members:
                    print(f"{member['username']} (User ID: {member['user_id']}): {share_per_member}")

                confirm = input("Confirm and add group expense? (yes/no): ").strip().lower()
                if confirm != "yes":
                    display_message("Group expense addition cancelled.")
                    continue

                shares = []
                for member in members:
                    shares.append({
                        'user_id': member['user_id'],
                        'share_amount': share_per_member
                    })

                GroupService.add_group_expense(group_id, user_id, amount, category, description, date, shares)
                display_message("Group expense and shares added successfully.")

            elif choice == "6":
                groups = GroupService.list_groups(user_id)
                if not groups:
                    continue
                try:
                    group_id = int(input("Enter group ID to view expenses: "))
                    GroupService.view_group_expenses(group_id)
                except ValueError:
                    display_message("Invalid group ID.")

            elif choice == "0":
                break

            else:
                display_message("Invalid option. Try again.")


from utils.print_service import display_message
from models.expense import Expense
from datetime import datetime

class ExpenseService:

    @staticmethod
    def add_expense(user_id):
        while True:
            try:
                amount = float(input("Enter amount: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

        while True:
            category = input("Enter category: ").strip()
            if not category:
                print("Category cannot be empty.")
                continue
            break

        while True:
            description = input("Enter description: ").strip()
            if not description:
                print("Description cannot be empty.")
                continue
            break

        while True:
            date = input("Enter date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please enter date as YYYY-MM-DD.")

        expense = Expense(user_id, amount, category, description, date)
        success = Expense.add_expense(expense)

        if success:
            display_message("Expense added successfully.")
        else:
            display_message("Failed to add expense.")

    @staticmethod
    def view_expenses(user_id):
        expenses = Expense.get_expenses_by_user(user_id)
        if not expenses:
            display_message("No expenses found.")
            return

        from utils.print_service import print_table, paginate_list

        headers = ['id', 'amount', 'category', 'description', 'date']
        pages = list(paginate_list(expenses, 5))
        for i, page in enumerate(pages, start=1):
            print(f"\nPage {i} of {len(pages)}")
            print_table(page, headers)
            if i < len(pages):
                input("Press Enter to see next page...")

    @staticmethod
    def update_expense(user_id):
        ExpenseService.view_expenses(user_id)

        while True:
            try:
                expense_id = int(input("Enter expense ID to update: "))
                if expense_id <= 0:
                    print("Invalid ID. Must be positive number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric expense ID.")

        while True:
            try:
                amount = float(input("Enter new amount: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

        while True:
            category = input("Enter new category: ").strip()
            if not category:
                print("Category cannot be empty.")
                continue
            break

        while True:
            description = input("Enter new description: ").strip()
            if not description:
                print("Description cannot be empty.")
                continue
            break

        while True:
            date = input("Enter new date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please enter date as YYYY-MM-DD.")

        success = Expense.update_expense(expense_id, user_id, amount, category, description, date)
        if success:
            display_message("Expense updated successfully.")
        else:
            display_message("Failed to update expense.")

    @staticmethod
    def delete_expense(user_id):
        ExpenseService.view_expenses(user_id)

        while True:
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                if expense_id <= 0:
                    print("Invalid ID. Must be positive number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric expense ID.")

        success = Expense.delete_expense(expense_id, user_id)
        if success:
            display_message("Expense deleted successfully.")
        else:
            display_message("Failed to delete expense.")

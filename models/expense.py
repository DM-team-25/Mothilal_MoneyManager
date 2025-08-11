from utils.db_connection import get_connection

class Expense:
    def __init__(self, user_id, amount, category, description, date):
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    @staticmethod
    def add_expense(expense):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO personal_expenses (user_id, amount, category, description, date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (expense.user_id, expense.amount, expense.category, expense.description, expense.date))
            connection.commit()
            return True
        except Exception as Exceptionhandel:
            print(f"Error adding expense: {Exceptionhandel}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_expenses_by_user(user_id):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM personal_expenses WHERE user_id = %s ORDER BY date DESC"
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return results
        except Exception as Exceptionhandel:
            print(f"Error fetching expenses: {Exceptionhandel}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_expense(expense_id, user_id, amount, category, description, date):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """
                UPDATE personal_expenses
                SET amount=%s, category=%s, description=%s, date=%s
                WHERE id=%s AND user_id=%s
            """
            cursor.execute(query, (amount, category, description, date, expense_id, user_id))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as Exceptionhandel:
            print(f"Error updating expense: {Exceptionhandel}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_expense(expense_id, user_id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = "DELETE FROM personal_expenses WHERE id=%s AND user_id=%s"
            cursor.execute(query, (expense_id, user_id))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as Exceptionhandel:
            print(f"Error deleting expense: {Exceptionhandel}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

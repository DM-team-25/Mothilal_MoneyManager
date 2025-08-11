
from utils.db_connection import get_connection
from utils.print_service import display_message

class GroupExpenseModel:

    @staticmethod
    def create_group(name, created_by):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM user_groups WHERE name = %s", (name,))
            if cursor.fetchone():
                return False

            cursor.execute(
                "INSERT INTO user_groups (name, created_by) VALUES (%s, %s)",
                (name, created_by)
            )
            connection.commit()
            return True
        except Exception as Exceptionhandel:
            print(f"Error creating group: {Exceptionhandel}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_group_by_name(name):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_groups WHERE name = %s", (name,))
            return cursor.fetchone()
        except Exception as Exceptionhandel:
            print(f"Error fetching group by name: {Exceptionhandel}")
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_groups_by_user(user_id):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT ug.id, ug.name
                FROM user_groups ug
                JOIN group_members gm ON ug.id = gm.group_id
                WHERE gm.user_id = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as Exceptionhandel:
            print(f"Error fetching groups by user: {Exceptionhandel}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def add_expense(group_id, paid_by_user_id, amount, category, description, date):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO group_expenses (group_id, paid_by_user_id, amount, category, description, date) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (group_id, paid_by_user_id, amount, category, description, date)
            )
            connection.commit()
            return cursor.lastrowid  # Return expense ID for shares
        except Exception as Exceptionhandel:
            print(f"Error adding group expense: {Exceptionhandel}")
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_expenses_by_group(group_id):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT ge.id, ge.paid_by_user_id, u.username, ge.amount, ge.category, ge.description, ge.date "
                "FROM group_expenses ge "
                "JOIN users u ON ge.paid_by_user_id = u.id "
                "WHERE ge.group_id = %s",
                (group_id,)
            )
            return cursor.fetchall()
        except Exception as Exceptionhandel:
            print(f"Error fetching group expenses: {Exceptionhandel}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()


class GroupMemberModel:

    @staticmethod
    def add_member(group_id, user_id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id FROM group_members WHERE group_id = %s AND user_id = %s",
                (group_id, user_id)
            )
            if cursor.fetchone():
                return False

            cursor.execute(
                "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
                (group_id, user_id)
            )
            connection.commit()
            return True
        except Exception as Exceptionhandel:
            print(f"Error adding member: {Exceptionhandel}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_members_by_group(group_id):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT gm.user_id, u.username "
                "FROM group_members gm "
                "JOIN users u ON gm.user_id = u.id "
                "WHERE gm.group_id = %s",
                (group_id,)
            )
            return cursor.fetchall()
        except Exception as Exceptionhandel:
            print(f"Error fetching group members: {Exceptionhandel}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def add_expense_shares(group_expense_id, shares):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            # shares is list of dicts: {'user_id': x, 'share_amount': y}
            for share in shares:
                cursor.execute(
                    "INSERT INTO group_expense_shares (group_expense_id, user_id, share_amount) "
                    "VALUES (%s, %s, %s)",
                    (group_expense_id, share['user_id'], share['share_amount'])
                )
            connection.commit()
            return True
        except Exception as Exceptionhandel:
            print(f"Error adding expense shares: {Exceptionhandel}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

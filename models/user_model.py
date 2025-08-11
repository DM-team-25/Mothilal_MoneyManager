
from utils.db_connection import get_connection

class UserModel:

    @staticmethod
    def get_user_by_username_and_password(username, password):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            return user
        except Exception as Exceptionhandel:
            print(f"Error fetching user: {Exceptionhandel}")
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_by_username(username):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Exception as Exceptionhandel:
            print(f"Error fetching user by username: {Exceptionhandel}")
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def insert_user(username, name, password):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return False, "Username already exists."

            cursor.execute(
                "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)",
                (username, name, password)
            )
            connection.commit()
            return True, "Registration successful!"
        except Exception as Exceptionhandel:
            print(f"Error inserting user: {Exceptionhandel}")
            return False, "Registration failed due to an error."
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_users():
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username FROM users")
            users = cursor.fetchall()
            return users
        except Exception as Exceptionhandel:
            print(f"Error fetching all users: {Exceptionhandel}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()

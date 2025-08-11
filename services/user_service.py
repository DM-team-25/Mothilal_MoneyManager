from models.user_model import UserModel
from utils.print_service import display_message

class UserService:

    @staticmethod
    def is_username_taken(username):
        user = UserModel.get_user_by_username(username)
        return user is not None

    @staticmethod
    def register_user(username, name, password):
        if UserService.is_username_taken(username):
            return "Username already exists."
        success, message = UserModel.insert_user(username, name, password)
        return message

    @staticmethod
    def authenticate_user(username, password):
        user = UserModel.get_user_by_username_and_password(username, password)
        if user:
            return True, user.get('id')
        else:
            return False, None

    @staticmethod
    def list_all_users():
        users = UserModel.get_all_users()
        if not users:
            display_message("No users found.")
            return []
        print("\nAvailable Users:")
        for user in users:
            print(f"ID: {user['id']}, Username: {user['username']}")
        return users

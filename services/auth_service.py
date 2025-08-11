from services.user_service import UserService

class AuthService:

    @staticmethod
    def login(username, password):
        return UserService.authenticate_user(username, password)

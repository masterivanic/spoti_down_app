
__all__ = ['']

from ..repository.user_repo import UserRepository
from ..repository.user_repo import DatabaseConnection
from ..models.User import User
from ..models.User import get_time_today
from crypto import SimpleEncryption

class UserController:

    user_repo = None
    db = DatabaseConnection()

    def __init__(self) -> None:
        self.user_repo = UserRepository(database=self.db)
    
    def register_user(self, user:User):
        """ register a user in db """

        is_register = None
        username =  user.get_username
        email = user.get_email
        user_found = self.user_repo.get_user_by_email(email=email)
        if not user_found:
            password = SimpleEncryption(user.get_password)._encrypt_url()
            last_login = user.get_last_login
            date_joined = user.get_date_joined
            value = (username, email, password, last_login, date_joined)
            self.user_repo.create_user(value)
            is_register = True
        return is_register
            
        
    def user_login(self, user:User):
        """ user login in app """

        is_login = None
        email = user.get_email
        password = user.get_password
        user_found = self.user_repo.get_user_by_email(email=email)
        if user_found:
            decrypt_pass = SimpleEncryption(url=None)._decrypt_url(user_found[3])
            if decrypt_pass == password:
                is_login = True
            else:
                is_login = False
        return is_login

    def update_user_last_login(self, email):
        user = self.user_repo.get_user_by_email(email)
        user_id = user[0]
        self.user_repo.update_user_last_login(
            user_id=user_id,
            last_login=get_time_today()
        )
        return user[1]
        
    def user_logout(user:User):
        pass



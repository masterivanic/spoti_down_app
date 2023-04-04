
from uuid import uuid1


class User:
    """
        Define user model of application.
    """
    
    def __init__(self, username, email, password) -> None:
        self.__user_id = int(uuid1())
        self.__username = username
        self.__email = email
        self.__password = password
        self.__last_login = None #datetime field
        self.__date_joined = None # datetime field
        self.__is_active = True
        self.__is_admin = False

    @property
    def get_username(self):
        return self.__username
    
    @property
    def get_email(self):
        return self.__email

    @property
    def get_password(self):
        return self.__password

    @property
    def get_last_login(self):
        return self.__last_login

    @property
    def get_date_joined(self):
        return self.__date_joined
    
    def is_user_active(self):
        return self.__is_active

    def is_user_admin(self):
        return self.__is_admin

    def set_last_login(self, last_login):
        self.__last_login = last_login

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def __str__(self) -> str:
        return f"{self.__username} -- {self.__user_id}"
    
        
class UserDTO(User):

    def __init__(self, *args, **kwargs) -> None:
        User.__init__(*args, **kwargs)
        self.user_api_keys = None

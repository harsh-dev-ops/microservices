import os
import re as regex
from passlib.context import CryptContext
from passlib.hash import sha256_crypt, pbkdf2_sha256

from app.api.utils.strings import StringUtils

from .exceptions import InvalidPassword
from app.conf.settings import settings
from app.database.postgres.models import User as UserModel
from app.database.postgres.crud import UserCrud

class Password:
    def __init__(self) -> None:
        self._ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def validate(self, password:str) -> bool:
        if len(password) < 8:
            raise InvalidPassword("Password must be more than 8 chanracter")
        elif not regex.search("[a-z]", password):
            raise InvalidPassword("Password must have atleast one letter")
        elif not regex.search("[1-9]", password):
            raise InvalidPassword("Password must have atleast one number")
        elif not regex.search("[~!@#$%^&*]", password):
            raise InvalidPassword("Password must have atleast one special character")
        elif regex.search(f"[\s]", password):
            raise InvalidPassword("Space must not be there")
        else:
            return True
    
    def hash(self, password:str) -> str:
        return pbkdf2_sha256.hash(password)
    
    def confirm(self, password:str, confirm_password:str) -> bool:
        
        if not (password == confirm_password):
            raise InvalidPassword("Passwords not matched!")
        
        if self.validate(password)  \
            and self.validate(confirm_password):
            return True
    
    def verify(self, password:str, hashed_password:str) -> bool:
        try:
            if not pbkdf2_sha256.verify(password, hashed_password):
                raise InvalidPassword("Incorrect password!")
            return True
        except Exception as e:
            raise InvalidPassword("Incorrect Password!")
         
    def random_password(self) -> str:
        password = StringUtils.random_string(
            length=10, 
            chars=True, 
            digits=True, 
            special_characters=True
            )
        return self.hash(password)
    
    
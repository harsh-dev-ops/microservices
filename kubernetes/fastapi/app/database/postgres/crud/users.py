from sqlalchemy.orm import Session

from .base import BaseCRUD
from ..models import User


class UserCrud(BaseCRUD):
    def __init__(self, Model=User):
        super().__init__(Model)
        
    async def get_by_email(self, db:Session, email:str) -> User:
        obj = db.query(self.Model).filter(self.Model.email == email).first()
        return obj
    
    async def get_by_phone(self, db:Session, phone:str) -> User:
        obj = db.query(self.Model).filter(self.Model.phone == phone).first()
        return obj
    
from sqlalchemy.orm import Session

from .base import BaseCRUD
from ..models import Group, UserGroups
from ..models.groups import RoleEnum


class GroupCrud(BaseCRUD):
    def __init__(self, Model=Group):
        super().__init__(Model)
        
    async def get_by_name(self, db:Session, name:str) -> Group:
        obj = db.query(self.Model).filter(self.Model.name == name).first()
        return obj

class UserGroups(BaseCRUD):
    def __init__(self, Model=UserGroups):
        super().__init__(Model)
    
    async def get_by_role(self, db:Session, role:str) -> UserGroups:
        obj = db.query(self.Model).filter(self.Model.name == role).first()
        return obj
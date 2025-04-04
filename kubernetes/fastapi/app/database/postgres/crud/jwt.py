from sqlalchemy.orm import Session

from .base import BaseCRUD
from ..models import JWT


class JwtCrud(BaseCRUD):
    def __init__(self, Model=JWT):
        super().__init__(Model)
        
    async def get_by_user_id(self, db, user_id:int) -> JWT:
        obj = db.query(self.Model).filter(self.Model.user_id == user_id).first()
        await self.missing_obj(obj, user_id)
        return obj
    
    async def get_by_access_key(self, db, access_key:str) -> JWT:
        obj = db.query(self.Model).filter(self.Model.access_key == access_key).first()
        await self.missing_obj(obj, access_key)
        return obj
    
    async def get_by_refresh_key(self, db, refresh_key: str) -> JWT:
        obj = db.query(self.Model).filter(self.Model.refresh_key == refresh_key).first()
        await self.missing_obj(obj, refresh_key)
        return obj
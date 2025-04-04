from httpx import delete
from sqlalchemy.orm import Session
from fastapi import status

from ..models.users import User
from .base import BaseCRUD
from ..models import Otp
from app.api.views.otp.exceptions import InvalidOtp


class OtpCrud(BaseCRUD):
    def __init__(self, Model=Otp):
        super().__init__(Model)
    
    async def get_by_otp(self, db:Session, otp:str) -> Otp:
        obj = db.query(self.Model).filter(self.Model.otp == otp).first()
        await self.missing_obj(obj, 0)
        if obj.is_expired:
            raise InvalidOtp("Otp has been expired!", status.HTTP_406_NOT_ACCEPTABLE)
        return obj
    
    async def get_by_email_or_phone(self, db:Session, email_or_phone:str):
        return db.query(self.Model).filter(self.Model.email_or_phone == email_or_phone).all()
    
    async def delete_previous_otp(self, db:Session, email_or_phone:str):
        all_obj = await self.get_by_email_or_phone(db, email_or_phone)
        for obj in all_obj:
            await self.delete(db, obj.id)
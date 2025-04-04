from fastapi import BackgroundTasks, status
from sqlalchemy.orm import Session

from app.api.views.otp.schema import OtpDBIn
from app.database.postgres import crud
from app.database.postgres.models import User

from ..users.exceptions import InvalidEmailId, MissingFormData, InvalidPhoneNumber
from .exceptions import InvalidOtp
from app.conf.exceptions import MethodDepericated
from .helpers import Otp
from app.api.email.schema import EmailSchema
from .schema import OtpIn, OtpSend


class OtpService():
    def __init__(self) -> None: 
        self._crud = crud.get('otp_crud')
        self._user_crud = crud.get('user_crud')
        self._otp = Otp()
        
    async def send_on_email(self, db: Session, user_obj: User, background_tasks: BackgroundTasks) -> OtpDBIn:
        
        if not user_obj.email:
            raise InvalidEmailId("Email Id not registered!", status.HTTP_404_NOT_FOUND)
        
        otp = self._otp.create()
        email = EmailSchema(email=[user_obj.email], body={"otp": otp}, subject="OTP")
        background_tasks.add_task(self._otp.send_email, email)
        
        return OtpDBIn(email_or_phone= user_obj.email, user_id=user_obj.id, otp=otp)
    
    async def send_on_phone(self, db: Session, user_obj: User, background_tasks: BackgroundTasks) -> OtpDBIn:

        if not user_obj.phone:
            raise InvalidPhoneNumber("Phone number not registered!", status.HTTP_404_NOT_FOUND)
        
        otp = self._otp.create()
        body = f"Your otp is {otp}"
        background_tasks.add_task(self._otp.send_sms, body, user_obj.phone)
        
        return OtpDBIn(email_or_phone= user_obj.phone, user_id=user_obj.id, otp=otp)
            
    async def send(self, db:Session, data:OtpSend, background_tasks: BackgroundTasks) -> dict:
        
        if data.email:
            user_obj = await self._user_crud.get_by_email(db, data.email)
            if not user_obj:
                user_obj = await self._user_crud.create(db, data.model_dump())
            otp_data = await self.send_on_email(db, user_obj, background_tasks)
            
        elif data.phone:
            raise MethodDepericated()
            user_obj = await self._user_crud.get_by_phone(db, data.phone)
            if not user_obj:
                user_obj = await self._user_crud.create(db, data.model_dump())
            otp_data = await self.send_on_phone(db, data, background_tasks)
        else:
            raise MissingFormData("Email or phone required to send otp!")
        
        await self._crud.delete_previous_otp(db, otp_data.email_or_phone)
        obj = await self._crud.create(db, otp_data.model_dump())
        
        response = {"message": "Otp sent successfully", "id": obj.id, "to": obj.email_or_phone}
        return response
    
    async def verify(self, db:Session, data: OtpIn, background_tasks: BackgroundTasks):
        
        obj = await self._crud.get_by_otp(db, data.otp)
        
        if '@' in obj.email_or_phone:
            if not obj.user.is_email_verified:
                await self._user_crud.update(db, obj.user_id, {'is_email_verified': True})
        else:
            if not obj.user.is_phone_verified:
                await self._user_crud.update(db, obj.user_id, {'is_phone_verified': True})
        
        if not obj:
            raise InvalidOtp("Otp not found!", status.HTTP_404_NOT_FOUND)
        
        user = obj.user
        
        await self._crud.delete(db, obj.id)
        # return {"message": "Otp verified successfully", "valid": True}
        return user
        
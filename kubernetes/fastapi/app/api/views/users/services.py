from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from .schema import UserRegisteration, UserLogin, UpdatePassword
from ..tokens.schema import CreateTokenOut
from ..otp.schema import OtpIn
from app.database.postgres import crud
from app.database.postgres.models import User
from . import helpers
from .exceptions import InvalidEmailId, MissingFormData
from ..tokens.services import Token
from ..otp.services import OtpService

class UserBase:
    def __init__(self) -> None:
        self._crud  = crud.get('user_crud')
        self._password_utils = helpers.Password()
        self.token_service = Token()
        self.otp_service = OtpService()

class User(UserBase):
    async def details(self, db:Session, user_id:int) -> User:
        return await self._crud.get(db, user_id)
    
    async def register(self, db:Session, data:UserRegisteration, background_tasks: BackgroundTasks | None = None) -> User:
        
        if await self._crud.get_by_email(db, data.email):
            raise InvalidEmailId("Email Id already exists!", status.HTTP_406_NOT_ACCEPTABLE)
        
        if data.password and data.confirm_password:
            self._password_utils.confirm(data.password, data.confirm_password)
            
        if not data.password:
            data.password = self._password_utils.random_password()
        
        data.password = self._password_utils.hash(data.password)
        
        user_data = data.model_dump(exclude_none=True)
        user_data.pop('confirm_password', None)
        user_obj = await self._crud.create(db, user_data)
        return user_obj
        
    async def login(self, db:Session, data:UserLogin, background_tasks: BackgroundTasks | None = None) -> CreateTokenOut:
        user_obj = await self._crud.get_by_email(db, data.email)
        if user_obj:
            if self._password_utils.verify(data.password, user_obj.password):
                return await self.token_service.generate(user_obj)
        else:
            raise InvalidEmailId("Email Id not registered!", status.HTTP_404_NOT_FOUND)
    
    async def login_by_otp(self, db:Session, data:OtpIn, background_tasks: BackgroundTasks) -> CreateTokenOut:
        obj  = await self.otp_service.verify(db, data, background_tasks)
        return await self.token_service.generate(obj)
    
    async def logout(self, token:str) -> None:
        await self.token_service.delete(token)
        return {'message': "User logged out"}
        
    async def update_password(self, db:Session, user_id:int, data:UpdatePassword, background_tasks: BackgroundTasks):
        self._password_utils.confirm(data.password, data.confirm_password)
        obj = await self._crud.update(db, user_id, {"password":self._password_utils.hash(data.password)})
        return {"message": "Password updated sucessfully!"} if obj else {"message": "Something went wrong!"}
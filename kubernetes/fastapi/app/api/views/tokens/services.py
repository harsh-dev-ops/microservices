from datetime import datetime, timezone
from typing import Any
from fastapi import status
from pydantic import AnyUrl

from app.database.redis.models.tokens import TokenModel

from .helpers import JWT
from .exceptions import TokenNotFound, TokenExpired, InvalidToken
from .schema import CreateTokenOut, RefreshTokenOut
from app.conf.settings import settings
from app.database.redis import crud
from app.database.postgres import crud as postgres_crud
from app.database.postgres.models import User



class Token:
    def __init__(self) -> None:
        self._jwt = JWT(
                secret_key = settings.SECRET_KEY,
                jwt_algorithm = settings.JWT_ALGORITHM,
                refresh_token_expires_in = settings.REFRESH_TOKEN_EXPIRES_IN,
                access_token_expires_in = settings.ACCESS_TOKEN_EXPIRES_IN
            )
        self._crud = crud.get('token_crud')
        self._user_crud = postgres_crud.get('user_crud')
        # self._crud = postgres_crud.get('jwt_crud')
        
    
    async def create_token_data(self, user_obj) -> dict:
        data = {
            "sub": str(user_obj.id),
            "email": user_obj.email,
            "is_verfied": user_obj.is_verified,
            "superuser": user_obj.superuser,
        }
        membership_list = []
        
        for membership in user_obj.membership:
            membership_list.append({
                "group_id": membership.group_id,
                "group_name": membership.group.name,
                "membership_id": membership.id,
                "role": membership.role.name,
                "add_members": membership.add_members,
                "view_members": membership.view_members,
                "remove_members": membership.remove_members,
                "edit_members": membership.edit_members,
                "edit_roles": membership.edit_roles,
                "buy_subscription": membership.buy_subscription,
                "edit_subscription": membership.edit_subscription,
                "view_subscription": membership.view_subscription,
                "edit_group": membership.edit_group,
            }) 
            
        data["membership"] = membership_list
        return data
    
    async def generate(self, user_obj: User) -> CreateTokenOut:
        
        user_id = str(user_obj.id)
        token_details = self._crud.get_by_user_id(user_id)
        
        if isinstance(token_details, list) or isinstance(token_details, tuple):
            for token in token_details:
                self._crud.delete(token.pk)
    
        data = await self.create_token_data(user_obj)
        print(data)
        
        refresh_token, refresh_token_data = await self._jwt.create_refresh_token(data)
        access_token, access_token_data = await self._jwt.create_access_token(data)
        
        token_obj = self._crud.create({
            'user_id': user_id,
            'access_key': access_token_data['access_key'],
            'refresh_key': refresh_token_data['refresh_key'],
            'refresh_token_exp_at': refresh_token_data['exp'],
            'access_token_exp_at': access_token_data['exp']
        })
        
        return CreateTokenOut(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='Bearer'
        )
    
    async def refresh(self, db, refresh_token:str) -> RefreshTokenOut:
        
        payload = self._jwt.decode_token(refresh_token)
        
        user_obj = await self._user_crud.get(db, int(payload['sub']))
        
        if not user_obj:
            raise InvalidToken("User Not Found!", status.HTTP_404_NOT_FOUND)
        
        token_obj = self._crud.get_by_refresh_key(refresh_key=payload['refresh_key'], 
                                                  user_id=payload['sub'])
        if not token_obj:
            raise TokenNotFound("Refresh Token Not Found in database!")
        
        if token_obj.refresh_token_exp_at < datetime.now(timezone.utc):
            raise TokenExpired("Refresh Token Expired!")
        
        data = payload
        for key in ['exp', 'refresh_key']:
            data.pop(key)
        
        access_token, access_token_data = await self._jwt.create_access_token(data)
        
        token_obj.access_token_exp_at = access_token_data['exp']
        token_obj.access_key = access_token_data['access_key']
        token_obj.save()
        
        return RefreshTokenOut(
            access_token=access_token, 
            token_type="Bearer"
            )
        
    async def get_details(self, token:str) -> dict:
        
        payload = self._jwt.decode_token(token)
        
        if payload['type'] != "access":
            raise InvalidToken("Token is not Access Token!")
        
        token_obj = self._crud.get_by_access_key(access_key=payload['access_key'], 
                                                 user_id=payload['sub'])
        if not token_obj:
            raise TokenNotFound("Access Token not found in Database!")
            
        if token_obj.access_token_exp_at < datetime.now(timezone.utc):
            raise TokenExpired("Access Token Expired!")
        
        payload['valid_token'] = True

        return payload
    
    async def delete(self, token:str) -> Any:
        payload = self._jwt.decode_token(token)
        token_obj: TokenModel = self._crud.get_by_access_key(access_key=payload['access_key'], 
                                                 user_id=payload['sub'])
        self._crud.delete(token_obj.pk)
        
        

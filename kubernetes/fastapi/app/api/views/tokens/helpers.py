from uuid import uuid4
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone


from app.conf.settings import settings
from .exceptions import InvalidToken

class JWT:
    def __init__(self,
                 secret_key:str,
                 jwt_algorithm:str,
                 refresh_token_expires_in: int,
                 access_token_expires_in: int
                 ) -> None:
        
        self._secret_key = secret_key
        self._algorithm = jwt_algorithm
        self._refresh_token_expires_in = refresh_token_expires_in
        self._access_token_expires_in = access_token_expires_in
        
    def create_token(self, data: dict) -> str:
        encoded_jwt = jwt.encode(data, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt
    
    def decode_token(self, token:str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, verify=True, algorithms=[self._algorithm])
            return payload
        except InvalidTokenError:
            raise InvalidToken()
        except Exception as e:
            print(e)
            raise InvalidToken()
    
    async def create_payload(self, data:dict, exp_duration:dict) -> dict:
        to_encode: dict = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(**exp_duration)
        to_encode.update({"exp": expire})
        return to_encode
    
    async def create_refresh_token(self, data: dict):
        data['refresh_key'] = str(uuid4())
        data['type'] = "refresh"
        token_data = await self.create_payload(
            data = data,
            exp_duration={'days': self._refresh_token_expires_in})
        token = self.create_token(token_data)
        return (token, token_data)
    
    async def create_access_token(self, data: dict):
        data['access_key'] = str(uuid4())
        data['type'] = "access"
        token_data = await self.create_payload(
            data = data,
            exp_duration={'minutes': self._access_token_expires_in})
        token = self.create_token(token_data)
        return (token, token_data)        

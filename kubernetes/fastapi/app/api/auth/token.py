from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.conf.settings import settings
from .schema import Token
from ..views.users import services, schema
from app.database.postgres.deps import db_dependency

router = APIRouter()

@router.post('/token')
async def login_access_token(
    request: Request, 
    response: Response, 
    db:db_dependency,
    user_form: Annotated[
        OAuth2PasswordRequestForm, 
        Depends()
        ] = None,) -> Token:
    
    user_service = services.User()
    
    payload = {
        'email': user_form.username,
        'password': user_form.password
    }
    
    user_data = schema.UserLogin(**payload)
    
    resp = await user_service.login(db, user_data)
    
    data = {
        'access_token': resp.access_token,
        'token_type': resp.token_type
    }
        
    return Token(**data)

        
    
from typing import Annotated
from fastapi import APIRouter, Query, Request, Response, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from app.database.postgres.deps import db_dependency
from . import services, schema
from ..tokens.schema import CreateTokenOut
from ..otp.schema import OtpIn
from app.api.auth.deps import token_details, get_token, oauth_token

router = APIRouter()

user_service = services.User()

@router.get('/me', response_model=schema.UserDetailsOut)
async def get_user_info(
    request: Request, 
    response: Response, 
    token_payload: token_details,
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    user_id = int(token_payload.sub)
    return await user_service.details(db, user_id)


@router.post('/register', status_code=201)
async def register_user(
    request: Request, 
    response: Response, 
    data: schema.UserRegisteration, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    user_obj = await user_service.register(db, data, background_tasks)
    return {"message": "User created successfully"} if user_obj else {"message": "Something went wrong"}


@router.post('/login', response_model=CreateTokenOut, status_code=status.HTTP_202_ACCEPTED)
async def user_login(
    request: Request, 
    response: Response, 
    data: schema.UserLogin, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    return await user_service.login(db, data, background_tasks)


@router.post('/login/otp', status_code=status.HTTP_201_CREATED, response_model=CreateTokenOut)
async def user_login(
    request: Request, 
    response: Response, 
    data: OtpIn, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    return await user_service.login_by_otp(db, data, background_tasks)

@router.post('/logout',status_code=status.HTTP_200_OK)
async def user_logout(
    request: Request, 
    response: Response,
    token: oauth_token,
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    return await user_service.logout(token)


@router.post('/update/password', status_code=status.HTTP_201_CREATED)
async def user_login(
    request: Request, 
    response: Response, 
    token_payload: token_details,
    data: schema.UpdatePassword, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    user_id = int(token_payload.sub)
    return await user_service.update_password(db, user_id, data, background_tasks)






from fastapi import APIRouter, Query, Request, Response, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from app.database.postgres.deps import db_dependency
from .schema import OtpSend, OtpIn
from . import services

otp_service = services.OtpService()

router = APIRouter()

@router.post('/send', status_code=status.HTTP_201_CREATED)
async def user_login(
    request: Request, 
    response: Response, 
    data: OtpSend, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    result = await otp_service.send(db, data, background_tasks)
    return result if result else {"message": "Something went wrong"}


@router.post('/verify', status_code=status.HTTP_200_OK)
async def verify_by_otp(
    request: Request, 
    response: Response, 
    data: OtpIn, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    result = await otp_service.verify(db, data, background_tasks)
    return {'message': "Otp verified!"} if result else {"message": "Otp not verified!"}
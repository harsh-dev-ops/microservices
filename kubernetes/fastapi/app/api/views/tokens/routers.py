from fastapi import APIRouter, Header, Request, Response, status

from .schema import RefreshTokenIn, RefreshTokenOut, CreateTokenOut, TokenDetails, TokenDetailsIn, UserDataIn
from . import services
from app.database.postgres.deps import db_dependency

router = APIRouter()

token_service = services.Token()

@router.post('/refresh', response_model = RefreshTokenOut, status_code=status.HTTP_201_CREATED)
async def generate(request: Request, response: Response,db: db_dependency, data: RefreshTokenIn):
    refresh_token: str = data.refresh_token
    return await token_service.refresh(db, refresh_token)


@router.post('/create', response_model=CreateTokenOut, deprecated=True, include_in_schema=False)
async def create_tokens(request: Request, response: Response, data: UserDataIn):
    user_data: dict = data.model_dump()
    return await token_service.generate(user_data)


@router.post('/details', response_model=TokenDetails, status_code=status.HTTP_200_OK)
async def access_token_details(request: Request, response: Response, data: TokenDetailsIn):
    access_token: str = data.access_token
    return await token_service.get_details(access_token)


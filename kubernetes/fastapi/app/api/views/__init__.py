from fastapi import APIRouter

from .otp.routers import router as otp_router
from .tokens.routers import router as token_router
from .users.routers import router as users_router
from .groups.routers import router as groups_router


api_router = APIRouter()

api_router.include_router(
    otp_router,
    prefix='/otp',
    tags=["OTP"],
)

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["User"],
)

api_router.include_router(
    groups_router,
    prefix='/groups',
    tags=['Group'],
)

api_router.include_router(
    token_router,
    prefix='/tokens',
    tags=["Token"]
)

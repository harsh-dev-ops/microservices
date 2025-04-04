from typing import List
from pydantic_settings import BaseSettings
from pydantic import EmailStr, Field,  AnyHttpUrl
from decouple import config
from datetime import datetime, timezone
import pytz

asia_timezone = pytz.timezone('Asia/Kolkata')

def current_datetime() -> datetime:
    return datetime.now(asia_timezone)

class Settings(BaseSettings):
    SECRET_KEY: str
    
    ENV: str
    DEBUG: bool
    
    POSTGRES_DB:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_PORT:str
    
    
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str
    ALLOWED_ORIGIN: List[str] = config('CLIENT_ORIGIN', cast=str).split(",")

    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_USE_TLS: bool
    EMAIL_FROM: str
    
    TWILIO_PHONE_NUMBER: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    
    SQLALCHEMY_DATABASE_URL_LOCAL: AnyHttpUrl = Field("sqlite:///db.sqlite", validate_default=False)
    
    SQLALCHEMY_DATABASE_URL_DEV: AnyHttpUrl = Field(
        f"postgresql+psycopg2://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}",
        validate_default=False
    )
    SQLALCHEMY_DATABASE_URL_PROD: AnyHttpUrl = Field(
        f"postgresql+psycopg2://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}",
        validate_default=False
    )
    
    REDIS_HOST:str
    REDIS_PORT:int
    REDIS_DB:int
    
    REDIS_BROKER_URL: str = Field(config('REDIS_BROKER_URL', cast=str, default="redis://localhost:6379/0"))
    REDIS_BACKEND_URL: str = Field(config('REDIS_BACKEND_URL', cast=str, default="redis://localhost:6379/0"))
    
    # Elastic search
    ELASTICSEARCH_HOSTS: str

    class Config:
        env_file = '.env'


settings = Settings()

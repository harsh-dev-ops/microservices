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
    SECRET_KEY: str = Field(config("SECRET_KEY", cast=str))
    
    ENV: str = Field(config("ENV", cast=str))
    DEBUG: bool = Field(config("DEBUG", cast=bool))
    
    POSTGRES_DB:str = Field(config("POSTGRES_DB", cast=str))
    POSTGRES_USER:str = Field(config("POSTGRES_USER", cast=str))
    POSTGRES_PASSWORD:str = Field(config("POSTGRES_PASSWORD", cast=str))
    POSTGRES_HOST:str = Field(config("POSTGRES_HOST", cast=str))
    POSTGRES_PORT: int = Field(config("POSTGRES_PORT", cast=int))
    
    
    REFRESH_TOKEN_EXPIRES_IN: int = Field(config("REFRESH_TOKEN_EXPIRES_IN", cast=int))
    ACCESS_TOKEN_EXPIRES_IN: int = Field(config("ACCESS_TOKEN_EXPIRES_IN", cast=int))
    JWT_ALGORITHM: str = Field(config("JWT_ALGORITHM", cast=str))

    CLIENT_ORIGIN: str = Field(config("CLIENT_ORIGIN", cast=str))
    ALLOWED_ORIGIN: List[str] = config('CLIENT_ORIGIN', cast=str).split(",")

    EMAIL_SERVER: str = Field(config("EMAIL_SERVER", cast=str))
    EMAIL_PORT: int = Field(config("EMAIL_PORT", cast=int))
    EMAIL_USERNAME: str = Field(config("EMAIL_USERNAME", cast=str))
    EMAIL_PASSWORD: str = Field(config("EMAIL_PASSWORD", cast=str))
    EMAIL_USE_TLS: bool = Field(config("EMAIL_USE_TLS", cast=bool))
    EMAIL_FROM: str = Field(config("EMAIL_FROM", cast=str))
    
    TWILIO_PHONE_NUMBER: str = Field(config("TWILIO_PHONE_NUMBER", cast=str))
    TWILIO_ACCOUNT_SID: str = Field(config("TWILIO_ACCOUNT_SID", cast=str))
    TWILIO_AUTH_TOKEN: str = Field(config("TWILIO_AUTH_TOKEN", cast=str))
    
    SQLALCHEMY_DATABASE_URL_LOCAL: AnyHttpUrl = Field("sqlite:///db.sqlite", validate_default=False)
    
    SQLALCHEMY_DATABASE_URL_DEV: AnyHttpUrl = Field(
        f"postgresql+psycopg2://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}",
        validate_default=False
    )
    SQLALCHEMY_DATABASE_URL_PROD: AnyHttpUrl = Field(
        f"postgresql+psycopg2://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}",
        validate_default=False
    )
    
    REDIS_HOST:str = Field(config("REDIS_HOST", cast=str))
    REDIS_PORT:int = Field(config("REDIS_PORT", cast=int))
    REDIS_DB:int = Field(config("REDIS_DB", cast=int))
    
    REDIS_BROKER_URL: str = Field(config('REDIS_BROKER_URL', cast=str, default="redis://localhost:6379/0"))
    REDIS_BACKEND_URL: str = Field(config('REDIS_BACKEND_URL', cast=str, default="redis://localhost:6379/0"))
    
    # Elastic search
    ELASTICSEARCH_HOSTS: str = Field(config("ELASTICSEARCH_HOSTS", cast=str))


settings = Settings()

from app.conf.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if settings.DEBUG:
    if settings.ENV=="local":
        DB_URI = settings.SQLALCHEMY_DATABASE_URL_LOCAL
    else:
        DB_URI = settings.SQLALCHEMY_DATABASE_URL_DEV
else:
    DB_URI = settings.SQLALCHEMY_DATABASE_URL_PROD

engine = create_engine(DB_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


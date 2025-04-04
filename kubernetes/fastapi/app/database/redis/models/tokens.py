from datetime import datetime
from redis_om import HashModel, Migrator, Field

from ..sessions import redis_db


class TokenModel(HashModel):
    user_id: str = Field(index=True)
    access_key: str = Field(index=True)
    refresh_key: str = Field(index=True)
    refresh_token_exp_at: datetime
    access_token_exp_at: datetime
    
    class Meta:
        database = redis_db
        
Migrator().run()
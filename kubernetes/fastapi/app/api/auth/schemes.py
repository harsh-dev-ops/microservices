from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

access_token = APIKeyHeader(name='X-Auth-Token')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/token')
from fastapi import Depends
from typing import Annotated

from . import schemes
from ..views.tokens import services
from ..views.tokens.schema import TokenDetails

token_service = services.Token()

get_token = Annotated[str, Depends(schemes.access_token)]

oauth_token = Annotated[str, Depends(schemes.oauth2_scheme)]

async def get_header_token_details(token: Annotated[str, Depends(schemes.access_token)]) -> TokenDetails:
    data = await token_service.get_details(token)
    return TokenDetails(**data)


async def get_oauth2_token_details(token: Annotated[str, Depends(schemes.oauth2_scheme)]) -> TokenDetails:
    data = await token_service.get_details(token)
    return TokenDetails(**data)

# API Header token Details
# token_details = Annotated[TokenDetails, Depends(get_header_token_details)]

# OAuth2 token Details
token_details = Annotated[TokenDetails, Depends(get_oauth2_token_details)]
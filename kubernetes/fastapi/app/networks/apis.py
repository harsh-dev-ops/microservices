from typing import Annotated
from typing_extensions import Doc
import aiohttp, async_timeout
from fastapi.exceptions import HTTPException
from fastapi import status


from app.conf.settings import settings


async def request(
    url: Annotated[str, Doc("Microservice url")],
    method: Annotated[str, Doc("GET, POST, PUT, PATCH, DELETE")],
    headers: Annotated[dict, Doc("Request headers for api")],
    payload: Annotated[dict, Doc("Data as json (dict) format for api")] = {},
    ):
    with async_timeout.timeout(settings.REQUEST_TIME_OUT):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            async with request(url, json=payload, headers=headers) as response:
                data = await response.json()
                return (data, response.status)
            
            
async def create_request(
    url: Annotated[str, Doc("Microservice url")],
    method: Annotated[str, Doc("GET, POST, PUT, PATCH, DELETE")],
    headers: Annotated[dict, Doc("Request headers for api")] = {"accept": "application/json"},
    payload: Annotated[dict, Doc("Data as json (dict) format for api")] = {},
    ):
    try:
        resp_data, status_code = await request(
            url=url,
            method=method,
            payload=payload,
            headers=headers,
        )
        
        if status_code >= 400:
            raise HTTPException(
                detail=resp_data.get('detail', 'Internal Server Error.'),
                status_code=status_code
            )
        return resp_data, status_code
    
    except aiohttp.client_exceptions.ClientConnectorError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service is unavailable.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except aiohttp.client_exceptions.ContentTypeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Service error.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
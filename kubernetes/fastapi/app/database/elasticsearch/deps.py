from typing import Annotated

from elasticsearch import AsyncElasticsearch
from .session import async_connections
from fastapi import Depends

async def get_es():
    es = async_connections.get_connection("default")
    try:
        yield es
    finally:
        await es.close()
        
es_dependency = Annotated[AsyncElasticsearch, Depends(get_es)]
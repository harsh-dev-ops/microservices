from elasticsearch_dsl import async_connections

from app.conf.settings import settings

try:
    async_connections.create_connection(alias="default", hosts=settings.ELASTIC_HOSTS, timeout=30)
except Exception as e:
    print(e)


from fastapi import APIRouter

from settings.configs import Settings
from cache.cachedriver import RedisConnector

router = APIRouter()
settings = Settings()
redis_connector = RedisConnector(settings)


@router.get("/get_from_redis")
async def get_redis():
    m = redis_connector.get("first")
    return m

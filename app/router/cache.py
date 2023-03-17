from fastapi import APIRouter
import datetime

from app.configuration.configs import Settings
from app.cache.cache_driver import RedisConnector
from app.cache.sub_strat import LRUStrategy

router = APIRouter()
settings = Settings()
redis_connector = RedisConnector(settings)


@router.get("/get/redis")
async def get_redis(key: str):
    return redis_connector.get(key)


@router.put("/set/redis")
async def set_redis(base_profile):
    return redis_connector.set(base_profile, LRUStrategy())

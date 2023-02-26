from fastapi import APIRouter

from settings.configs import Settings
from cache.cache_driver import RedisConnector
from cache.sub_strat import LRUStrategy

router = APIRouter()
settings = Settings()
redis_connector = RedisConnector(settings)


@router.get("/get/redis")
async def get_redis(base_profile):
    return redis_connector.get(base_profile)


@router.put("/set/redis")
async def set_redis(base_profile, sub_strt: LRUStrategy):
    return redis_connector.set(base_profile, sub_strt)

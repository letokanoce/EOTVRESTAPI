import base64
import json
import pickle

from fastapi import APIRouter, Depends, Body

from app.cache.cache_driver import RedisConnector
from app.cache.sub_strat import LRUStrategy
from app.configuration.configs import Settings

router = APIRouter()
settings = Settings()


def get_redis_connector():
    return RedisConnector(settings)


@router.get("/get/redis")
async def get_from_redis(entity: str, redis_connector: RedisConnector = Depends(get_redis_connector)):
    decoded_data_bytes = base64.b64decode((json.loads(entity))['data'].encode('utf-8'))
    entity_object = pickle.loads(decoded_data_bytes)
    result = redis_connector.get(entity_object)
    return result


@router.post("/set/redis")
async def set_to_redis(entity: str = Body(..., embed=True),
                       redis_connector: RedisConnector = Depends(get_redis_connector)):
    decoded_data_bytes = base64.b64decode((json.loads(entity))['data'].encode('utf-8'))
    entity_object = pickle.loads(decoded_data_bytes)
    result = redis_connector.set(entity_object, LRUStrategy())
    return result


@router.delete("/flush/redis")
async def set_to_redis(redis_connector: RedisConnector = Depends(get_redis_connector)):
    return redis_connector.clear()

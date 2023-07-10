import base64
import json
import pickle
from typing import Union

from fastapi import APIRouter, Body, Query

from app.cache.searializer import PickleSerializer
from app.cache.sub_strategy import LRUStrategy
from app.handler.cache_handler import RedisHandler
from app.instance import redis_client

router = APIRouter()
redis_handler = RedisHandler(redis_client, PickleSerializer())


@router.get("/get/redis")
async def get_from_redis(entity: Union[str, None] = Query()):
    decoded_data_bytes = base64.b64decode((json.loads(entity))['data'].encode('utf-8'))
    entity_object = pickle.loads(decoded_data_bytes)
    result = redis_handler.get(entity_object)
    return result


@router.post("/set/redis")
async def set_to_redis(entity: str = Body(..., embed=True)):
    decoded_data_bytes = base64.b64decode((json.loads(entity))['data'].encode('utf-8'))
    entity_object = pickle.loads(decoded_data_bytes)
    result = redis_handler.set(entity_object, LRUStrategy())
    return result


@router.delete("/flush/redis")
async def flush_redis():
    redis_handler.clear()
    return f"Flush Cache successfully"

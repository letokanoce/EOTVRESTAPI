import base64
import json

from redis.client import Redis

from app.cache.searializer import ISerializer
from app.cache.sub_strategy import ISubStrategy
from app.db.cache_driver import RedisDriver
from app.epbelsys.model import *


class RedisHandler:
    # Initialize RedisHandler
    def __init__(self, cache_driver: RedisDriver, serializer: ISerializer):
        self.client = cache_driver.client
        self.serializer = serializer

    # Get value associated with a key
    def get(self, base_profile: BaseProfile):
        key = self._generate_key(base_profile=base_profile)
        try:
            entity_exists, entity = self._level_exists_in_cache(client=self.client, key=key, base_profile=base_profile)
            print(f"entity is: {entity}")
            if entity_exists:
                print(f"value already exists in cache")
                return self._convert_to_json(entity)
            else:
                return json.dumps({'data': ""})
        except Exception as e:
            print(f"Error occurred while finding the value for key '{key}': {e}")

    # Set key-value pair in the cache
    def set(self, base_profile: BaseProfile, strategy: ISubStrategy):
        key = self._generate_key(base_profile)
        try:
            if not self.client.exists(key):
                self.client.hset(name=key, key=base_profile.sub_level,
                                 value=self.serializer.serialize(base_profile))
                print(f"added new value to cache")
                return
            entity_exists, _ = self._level_exists_in_cache(self.client, key, base_profile)
            if entity_exists:
                print(f"value already exists in cache")
                return
            self._add_or_replace_value(self.client, key, base_profile, strategy)
        except Exception as e:
            print(f"Error occurred while setting the hash value for key '{key}': {e}")

    # Clear all key-value pairs in the cache
    def clear(self):
        try:
            self.client.flushall()
            print("All keys and values have been cleared from the cache.")
        except Exception as e:
            print(f"Error occurred while clearing the cache: {e}")

    def _level_exists_in_cache(self, client: Redis, key: str, base_profile: BaseProfile):
        values = client.hvals(name=key)
        matched_entity = [self.serializer.deserialize(data=val) for val in values if
                          self.serializer.deserialize(data=val).sub_level == base_profile.sub_level]
        print(f"matched entity is: {matched_entity}")
        entity_exists = any(matched_entity)
        return entity_exists, matched_entity[0] if entity_exists else None

    def _add_or_replace_value(self, client: Redis, key: str, base_profile: BaseProfile, strategy):
        values = client.hvals(name=key)
        if len(values) < 2:
            client.hset(name=key, key=base_profile.sub_level, value=self.serializer.serialize(base_profile))
            print('added new value to cache')
        else:
            print('replacing value in cache')
            strategy.replace(key, base_profile, client)

    def _convert_to_json(self, base_profile: BaseProfile):
        entity_bytes = self.serializer.serialize(obj=base_profile)
        entity_base64 = base64.b64encode(entity_bytes).decode('utf-8')
        entity_json_data = json.dumps({'data': entity_base64})
        return entity_json_data

    @staticmethod
    def _generate_key(base_profile: BaseProfile):
        return base_profile.category + base_profile.env_settings.context + base_profile.env_settings.meaning

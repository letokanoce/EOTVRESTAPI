from abc import ABC, abstractmethod

import redis

from app.cache.cache_handler import CacheHandler
from app.cache.sub_strat import ISubStrategy
from app.configuration.configs import Settings
from app.epbelsys.model import BaseProfile


class CacheConnection(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, base_profile: BaseProfile):
        pass


class RedisConnector(CacheConnection):
    def __init__(self, settings):
        super().__init__(settings)
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=0
        )
        self.cache_handler = CacheHandler(self.pool)

    def get(self, base_profile: BaseProfile):
        return self.cache_handler.get(base_profile)

    def set(self, base_profile: BaseProfile, strategy: ISubStrategy):
        self.cache_handler.set(base_profile, strategy)

    def clear(self):
        self.cache_handler.clear()

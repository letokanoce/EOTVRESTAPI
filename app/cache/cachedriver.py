import redis

from abc import ABC, abstractmethod

from settings.configs import Settings


class CacheConnection(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self):
        pass


class RedisConnector(CacheConnection):

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.driver = self.create_driver()

    def create_driver(self):
        return redis.Redis(self.settings.REDIS_HOST, self.settings.REDIS_PORT,
                           0, self.settings.REDIS_PASSWORD)

    def get(self, key: str):
        return self.driver.get(key)

    def set(self, key: str, value: str):
        self.driver.set(key, value)
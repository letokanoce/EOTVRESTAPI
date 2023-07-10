from abc import ABC, abstractmethod
from typing import TypeVar

import redis

from app.configuration.configs import Settings, RedisSettings

# Define Type Variable T bounded by Settings class
T = TypeVar("T", bound=Settings)


class CacheConnection(ABC):
    # Abstract Base Class for Cache Connections
    def __init__(self, settings: T):
        self.settings = settings

    @abstractmethod
    def set_connection(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass


class RedisDriver(CacheConnection):
    def __init__(self, settings: RedisSettings):
        super().__init__(settings)
        self.client = self.set_connection()

    def set_connection(self):
        # Set up a Redis connection
        try:
            # Create a Redis connection pool
            connection_pool = redis.ConnectionPool(host=self.settings.REDIS_HOST,
                                                   port=self.settings.REDIS_PORT,
                                                   password=self.settings.REDIS_PASSWORD,
                                                   db=0)
            # Create a Redis client
            client = redis.Redis(connection_pool=connection_pool)
            if client.ping():
                print("Redis connection set successfully!")
            return client
        except Exception as e:
            print(f"Error occurred while setting up Redis connection: {e}")
            return None

    def close_connection(self):
        # Close the Redis connection
        try:
            self.client.close()
            print("Redis connection closed successfully!")
        except Exception as e:
            print(f"Error occurred while closing Redis connection: {e}")

import redis
import pickle
import datetime

from abc import ABC, abstractmethod
from app.configuration.configs import Settings
from app.cache.sub_strat import ISubStrategy


class CacheConnection(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, base_profile):
        pass


class RedisConnector(CacheConnection):

    def __init__(self, settings):
        super().__init__(settings)
        self.conn_pool = self.create_pool()

    def create_pool(self):
        return redis.ConnectionPool(host=self.settings.REDIS_HOST,
                                    port=self.settings.REDIS_PORT,
                                    password=self.settings.REDIS_PASSWORD,
                                    db=0)

    def get(self, key):
        with redis.Redis(connection_pool=self.conn_pool) as connection:
            data = connection.hgetall(key)
            if data:
                return [pickle.loads(val) for val in data.values()]
            else:
                return []

    def set(self, base_profile, strategy: ISubStrategy):
        key = base_profile.category + base_profile.environment.context + base_profile.environment.meaning
        with redis.Redis(connection_pool=self.conn_pool) as connection:
            if connection.exists(key):
                values = connection.hvals(key)
                if any(
                        pickle.loads(val).sub_level == base_profile.sub_level
                        for val in values):
                    print('value already exists in cache')
                else:
                    if len(values) < 10:
                        connection.hset(key, base_profile.sub_level,
                                        pickle.dumps(base_profile))
                        print('added new value to cache')
                    else:
                        print('replacing the value in cache')
                        strategy.replace(key, base_profile, connection)
            else:
                connection.hset(key, base_profile.sub_level,
                                pickle.dumps(base_profile))
                print('added new value to cache')

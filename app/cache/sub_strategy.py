import pickle
from abc import ABC, abstractmethod

from app.epbelsys.model import *


class ISubStrategy(ABC):
    @abstractmethod
    def replace(self, key: str, base_profile: BaseProfile, redis_conn):
        pass


class LRUStrategy(ISubStrategy):
    def replace(self, key: str, base_profile: BaseProfile, redis_conn):
        # get all values for the given key
        values = redis_conn.hvals(key)

        # sort the values based on the last access time
        sorted_values = sorted(values, key=lambda x: pickle.loads(x).last_acc_time)

        # if there are less than 10 values, add the new one
        # remove the least recently used value
        redis_conn.hdel(key, pickle.loads(sorted_values[0]).sub_class_level)
        # add the new value
        redis_conn.hset(key, base_profile.sub_class_level, pickle.dumps(base_profile))

import pickle
from abc import ABC, abstractmethod


class ISubStrategy(ABC):

    @abstractmethod
    def substitute(self, key: str, base_profile, redis_conn):
        pass


class LRUStrategy(ISubStrategy):

    def substitute(self, key: str, base_profile, redis_conn):
        # get all values for the given key
        values = redis_conn.hvals(key)
        # sort the values based on the last access time
        sorted_values = sorted(values,
                               key=lambda x: pickle.loads(x).last_acc_time)
        # remove the least recently used value
        redis_conn.hdel(key, pickle.loads(sorted_values[0]).sub_level)
        # add the new object
        redis_conn.hset(key, base_profile.sub_level,
                        pickle.dumps(base_profile))

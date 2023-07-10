import pickle
from abc import ABC, abstractmethod


class ISerializer(ABC):
    @abstractmethod
    def serialize(self, obj: object):
        pass

    @abstractmethod
    def deserialize(self, data: bytes):
        pass


class PickleSerializer(ISerializer):
    def serialize(self, obj: object):
        return pickle.dumps(obj)

    def deserialize(self, data: bytes):
        return pickle.loads(data)

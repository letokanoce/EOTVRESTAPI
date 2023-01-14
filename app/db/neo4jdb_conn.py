from abc import ABC, abstractmethod
from neo4j import GraphDatabase

from settings.configs import Settings


class DBConnection(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def create_driver(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_session(self):
        pass


class Neo4jConnector(DBConnection):

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.driver = self.create_driver()

    def create_driver(self):
        return GraphDatabase.driver(self.settings.NEO4J_URI,
                                    auth=(self.settings.NEO4J_USERNAME,
                                          self.settings.NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def get_session(self):
        return self.driver.session()
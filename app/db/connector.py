from abc import ABC, abstractmethod

from neo4j import GraphDatabase

from app.configuration.configs import SettingsT


class DbConnection(ABC):
    def __init__(self, settings: SettingsT):
        self.settings = settings

    @abstractmethod
    def set_connection(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def create_session(self):
        pass


class Neo4jDriver(DbConnection):
    def __init__(self, settings, max_pool_size):
        super().__init__(settings)
        self.pool_size = max_pool_size
        self.driver = self.set_connection()

    def set_connection(self):
        try:
            driver = GraphDatabase.driver(uri=self.settings.NEO4J_URI,
                                          auth=(self.settings.NEO4J_USERNAME, self.settings.NEO4J_PASSWORD),
                                          max_connection_pool_size=self.pool_size)
            print("Neo4j connection established successfully")
            return driver
        except Exception as e:
            raise ConnectionError(f"Error occurred while setting up Neo4j connection: {e}")

    def close_connection(self):
        try:
            self.driver.close()
            print("Neo4j connection closed successfully")
        except Exception as e:
            raise ConnectionError(f"Error occurred while closing Neo4j connection: {e}")

    def create_session(self):
        return self.driver.session()

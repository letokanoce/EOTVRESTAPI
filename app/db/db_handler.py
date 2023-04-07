from abc import ABC, abstractmethod
from typing import Union

from fastapi import HTTPException
from neo4j import Session

from app.utils.data_formatter import IProcessData


class Neo4jHandler(ABC):

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def run_cypher(self, cypher: str, parameters: dict):
        pass


class Neo4jQuerier(Neo4jHandler):

    def __init__(self, session: Session, processor: IProcessData):
        super().__init__(session)
        self.data_processor = processor

    def run_cypher(self, cypher: str, parameters: dict) -> Union[list, None]:
        with self.session.begin_transaction() as tx:
            query_results = tx.run(cypher, parameters).data()
            result = self.data_processor.process(query_results)
            if result is not None:
                return result
            raise HTTPException(status_code=404, detail=f"{parameters} not found")


class Neo4jPoster(Neo4jHandler):

    def __init__(self, session: Session, processor: IProcessData):
        super().__init__(session)
        self.data_processor = processor

    def run_cypher(self, cypher: str, parameters: dict) -> Union[list, None]:
        with self.session.begin_transaction() as tx:
            post_results = tx.run(cypher, parameters).data()
            result = post_results
            if result is not None:
                return result
            raise HTTPException(status_code=404, detail=f"{parameters} not found")

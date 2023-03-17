from abc import ABC, abstractmethod
from neo4j import Session
from fastapi import HTTPException
from typing import Union

from app.utils.dataproc import IProcessData


class Neo4jHandler(ABC):

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def run_cypher(self):
        pass


class Neo4jQueryer(Neo4jHandler):

    def __init__(self, session: Session, processor: IProcessData):
        super().__init__(session)
        self.data_processor = processor

    def run_cypher(self, cypher: str, parameters: dict) -> Union[list, None]:
        query_results = self.session.run(cypher, parameters).data()
        print("query_result", query_results)
        print("querytype", type(query_results))
        result = self.data_processor.process(query_results)
        print("processed result", result)
        if result is not None:
            return result
        raise HTTPException(status_code=404, detail=f"{parameters} not found")


class Neo4jPoster(Neo4jHandler):

    def __init__(self, session: Session, processor: IProcessData):
        self.session = session
        self.data_processor = processor

    def run_cypher(self, cypher: str, parameters: dict) -> Union[list, None]:
        post_results = self.session.run(cypher, parameters).data()
        result = post_results
        if result is not None:
            return result
        raise HTTPException(status_code=404, detail=f"{parameters} not found")

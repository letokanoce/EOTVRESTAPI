from neo4j import Session
from fastapi import HTTPException
from typing import Union

from utils.data_process import IProcessData


class Neo4jQueryer():

    def __init__(self, session: Session, processor: IProcessData, key: str):
        self.session = session
        self.data_processor = processor
        self.key = key

    def run_query(self, query: str, parameters: dict) -> Union[list, None]:
        query_results = self.session.run(query, parameters).data()
        result = self.data_processor.process(query_results, self.key)
        if result is not None:
            return result
        raise HTTPException(status_code=404, detail=f"{parameters} not found")

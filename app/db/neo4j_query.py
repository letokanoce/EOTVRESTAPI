from typing import Union
from neo4j import Session

from db.neo4j_handler import Neo4jQueryer
from utils.data_process import MatrixProcessor
from cypher.query import *


class Neo4jQueryHandler:

    def __init__(self, session: Session):
        self.session = session

    def get_sub_ids_list(self,
                         category: str = None,
                         sub_level: int = 1,
                         context: str = "reality",
                         meaning: str = "literal"):
        query = Neo4jQueryer(self.session, MatrixProcessor(), 'r')
        if category:
            query_results = query.run_query(
                GET_N_ID, {
                    "class": category,
                    "context": context,
                    "meaning": meaning,
                    "hop": sub_level
                })
            return query_results
        else:
            return []

    def get_sub_features(self, id_list: Union[list[int], None] = None):
        query = Neo4jQueryer(self.session, MatrixProcessor(), 'r')
        if id_list:
            query_results = query.run_query(GET_N_FEATURES,
                                            {"id_list": id_list})
            return query_results
        else:
            return []
from neo4j import Session

from db.db_handler import Neo4jPoster
from utils.dataproc import IProcessData
from cypher.post_cypher import *


class Neo4jPostHandler:

    def __init__(self, session: Session, processor: IProcessData):
        self.session = session
        self.poster = self._init_queryer(processor)

    def _init_queryer(self, processor: IProcessData):
        return Neo4jPoster(self.session, processor)

    def create_node(self,
                    category: str = None,
                    context: str = "reality",
                    meaning: str = "figurative",
                    descriptions: dict = {}):
        if category:
            post_results = self.poster.run_cypher(
                NEW_NODE, {
                    "class": category,
                    "context": context,
                    "meaning": meaning,
                    "add_params": descriptions
                })
        else:
            post_results = []

        self.session.close()
        return post_results
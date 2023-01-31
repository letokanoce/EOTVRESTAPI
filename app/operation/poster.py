from neo4j import Session

from db.dbhandle import Neo4jPoster
from utils.dataproc import StringProcessor
from cypher.postcypher import *


class Neo4jPostHandler:

    def __init__(self, session: Session):
        self.session = session
        self.poster = Neo4jPoster(session, StringProcessor())

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
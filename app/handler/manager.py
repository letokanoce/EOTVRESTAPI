from neo4j import Session

from app.executor.querier import QueryHandler
from app.handler.neo4j_handler import Neo4jHandler


class Neo4jContextManager:
    HANDLER_MAPPING = {
        'querier': QueryHandler,
        'poster': Neo4jHandler,
        'updater': Neo4jHandler,
        'deleter': Neo4jHandler,
    }

    def __init__(self, session: Session, handler_class: str = None):
        self.session = session
        self.handler_class = handler_class

    def __enter__(self):
        self.transaction = self.session.begin_transaction()
        handler = self.HANDLER_MAPPING.get(self.handler_class, Neo4jHandler)
        return handler(self.transaction)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                self.transaction.commit()
            except Exception as e:
                self.transaction.rollback()
                raise ConnectionError(f"Error occurred while committing Neo4j transaction: {e}")
        else:
            self.transaction.rollback()
        self.session.close()

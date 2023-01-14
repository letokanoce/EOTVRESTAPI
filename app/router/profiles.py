from fastapi import APIRouter, Depends, Query
from typing import Union
from neo4j import Session

from settings.configs import Settings
from db.neo4jdb_conn import Neo4jConnector
from db.neo4j_query import Neo4jQueryHandler
from cypher.query import *

router = APIRouter()
settings = Settings()
neo4j_connector = Neo4jConnector(settings)


@router.get("/n_ids", response_description="Get N Sub Level Entities IDs List")
async def get_n_subids(category: str = None,
                       sub_level: int = 1,
                       context: str = "reality",
                       meaning: str = "literal",
                       session: Session = Depends(
                           neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_ids_list(category, sub_level, context,
                                          meaning)


@router.get("/n_features",
            response_description="Get N Sub Level Features List")
async def get_n_subfeatures(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_features(id_list)

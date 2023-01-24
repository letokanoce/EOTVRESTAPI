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


@router.get("/n_feature",
            response_description="Get N Sub Level Feature")
async def get_n_sub_feature(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_feature(id_list)


@router.get("/n_pvalue", response_description="Get N Sub Level P Value")
async def get_sub_n_pval(id_list: Union[list[int], None] = Query(default=None),
                         session: Session = Depends(
                             neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_pval(id_list)


@router.get("/n_weight", response_description="Get N Sub Level Weight")
async def get_sub_n_wgt(id_list: Union[list[int], None] = Query(default=None),
                        session: Session = Depends(
                            neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_wgt(id_list)

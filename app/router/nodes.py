from typing import Union

from fastapi import APIRouter, Body, Depends, Query
from neo4j import Session

from app.configuration.configs import Settings
from app.db.db_driver import Neo4jConnector
from app.handler.poster import Neo4jPostHandler
from app.handler.querier import Neo4jQueryHandler
from app.utils.data_formatter import StringProcessor, MatrixProcessor

router = APIRouter()
settings = Settings()
neo4j_connector = Neo4jConnector(settings)


@router.post("/create/node", response_description="Create a node")
async def create_node(category: str = Body(None, embed=True),
                      context: str = Body("reality", embed=True),
                      meaning: str = Body("figurative", embed=True),
                      descriptions: dict = Body({}, embed=True),
                      session: Session = Depends(neo4j_connector.get_session)):
    neo4j_post_handler = Neo4jPostHandler(session, StringProcessor())
    return neo4j_post_handler.create_node(category, context, meaning,
                                          descriptions)


@router.get("/feature", response_description="Get N Sub Level Feature")
async def get_n_sub_feature(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor())
    return query_handler.query_feature(id_list)[0]


@router.get("/pvalue", response_description="Get N Sub Level P Value")
async def get_sub_n_pval(id_list: Union[list[int], None] = Query(default=None),
                         session: Session = Depends(
                             neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor())
    return query_handler.query_pval(id_list)[0]


@router.get("/weight", response_description="Get N Sub Level Weight")
async def get_sub_n_wgt(id_list: Union[list[int], None] = Query(default=None),
                        session: Session = Depends(
                            neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor())
    return query_handler.query_wgt(id_list)[0]

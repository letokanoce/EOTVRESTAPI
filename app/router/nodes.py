from fastapi import APIRouter, Body, Depends, Query
from typing import Union
from neo4j import Session

from configuration.configs import Settings
from db.db_driver import Neo4jConnector
from handler.queryer import Neo4jQueryHandler
from handler.poster import Neo4jPostHandler
from utils.dataproc import StringProcessor, MatrixProcessor

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


@router.get("/n/feature", response_description="Get N Sub Level Feature")
async def get_n_sub_feature(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    return query_handler.query_feature(id_list)


@router.get("/n/pvalue", response_description="Get N Sub Level P Value")
async def get_sub_n_pval(id_list: Union[list[int], None] = Query(default=None),
                         session: Session = Depends(
                             neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    return query_handler.query_pval(id_list)


@router.get("/n/weight", response_description="Get N Sub Level Weight")
async def get_sub_n_wgt(id_list: Union[list[int], None] = Query(default=None),
                        session: Session = Depends(
                            neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    return query_handler.query_wgt(id_list)
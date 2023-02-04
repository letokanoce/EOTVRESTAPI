from fastapi import APIRouter, Body, Depends, Query
from typing import Union
from neo4j import Session

from settings.configs import Settings
from db.dbdriver import Neo4jConnector
from operation.queryer import Neo4jQueryHandler
from operation.poster import Neo4jPostHandler
from utils.dataproc import MatrixProcessor

router = APIRouter()
settings = Settings()
neo4j_connector = Neo4jConnector(settings)


@router.post("/create_node", response_description="Create a node")
async def create_node(category: str = Body(None, embed=True),
                      context: str = Body("reality", embed=True),
                      meaning: str = Body("figurative", embed=True),
                      descriptions: dict = Body({}, embed=True),
                      session: Session = Depends(neo4j_connector.get_session)):
    neo4j_post_handler = Neo4jPostHandler(session)
    return neo4j_post_handler.create_node(category, context, meaning,
                                          descriptions)


@router.get("/n_feature", response_description="Get N Sub Level Feature")
async def get_n_sub_feature(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    return query_handler.get_sub_feature(id_list)


@router.get("/n_pvalue", response_description="Get N Sub Level P Value")
async def get_sub_n_pval(id_list: Union[list[int], None] = Query(default=None),
                         session: Session = Depends(
                             neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    return query_handler.get_sub_pval(id_list)


@router.get("/n_weight", response_description="Get N Sub Level Weight")
async def get_sub_n_wgt(id_list: Union[list[int], None] = Query(default=None),
                        session: Session = Depends(
                            neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    return query_handler.get_sub_wgt(id_list)
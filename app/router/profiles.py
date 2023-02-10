from fastapi import APIRouter, Depends, Query
from typing import Union
from neo4j import Session

from settings.configs import Settings
from db.dbdriver import Neo4jConnector
from operation.queryer import Neo4jQueryHandler
from utils.dataproc import MatrixProcessor

router = APIRouter()
settings = Settings()
neo4j_connector = Neo4jConnector(settings)


@router.get("/n_ids", response_description="Get N Sub Level Entities IDs List")
async def get_n_sub_ids(category: str = None,
                        sub_class_level: int = 1,
                        context: str = "reality",
                        meaning: str = "literal",
                        session: Session = Depends(
                            neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    result = (query_handler.get_sub_ids(category, sub_class_level, context,
                                        meaning))[0]
    id_list = result[0]
    parent_node_id = result[1]
    n_level = result[2]
    return id_list, parent_node_id, n_level


@router.get(
    "/n_pval_corr_elems",
    response_description="Get N Sub Level P Value Correlations Elements")
async def get_n_pval_cov_elems(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    return query_handler.get_sub_pval_corr_elems(id_list)


@router.get("/n_level", response_description="Get N Level")
async def get_n_level(parent_id: int = None,
                      id_list: Union[list[int], None] = Query(default=None),
                      session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor(), 'r')
    result = (query_handler.get_level(parent_id, id_list))[0]
    sub_level_list = result[0]
    relative_wgt = result[1]
    return sub_level_list, relative_wgt

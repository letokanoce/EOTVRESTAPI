from typing import Union

from fastapi import APIRouter, Depends, Query
from neo4j import Session

from app.configuration.configs import Settings
from app.db.db_driver import Neo4jConnector
from app.handler.queryer import Neo4jQueryHandler
from app.utils.data_formatter import MatrixProcessor

router = APIRouter()
settings = Settings()
neo4j_connector = Neo4jConnector(settings)


@router.get("/n/ids_rel", response_description="Get N Sub Level Entities IDs List")
async def get_n_sub_ids(category: str = None,
                        sub_class_level: int = 1,
                        context: str = "reality",
                        meaning: str = "literal",
                        session: Session = Depends(
                            neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor())
    result = (query_handler.query_ids_rel(category, sub_class_level, context, meaning))
    '''
    params: id_list
            parent_node_id
            n_level
    '''
    return result[1], result[0], result[2]


@router.get("/n/pval/corr", response_description="Get N Sub Level P Value Correlations Elements")
async def get_n_pval_corr(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor())
    return query_handler.query_pval_corr_elems(id_list)


@router.get("/n/wgt/cov/co", response_description="Get N Sub Level P Value Covariance Coefficients Elements")
async def get_n_wgt_cov_co(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor())
    return (query_handler.query_wgt_cov_co(id_list))[0]


@router.get("/n/wgt/cov/sdpro", response_description="Get N Sub Level P Value Covariance SD Products Elements")
async def get_n_wgt_cov_sd_pro(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session, MatrixProcessor())
    return (query_handler.query_wgt_cov_sd_pro(id_list))[0]

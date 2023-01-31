from fastapi import APIRouter, Depends, Query
from typing import Union
from neo4j import Session

from settings.configs import Settings
from db.dbdriver import Neo4jConnector
from operation.queryer import Neo4jQueryHandler

router = APIRouter()
settings = Settings()
neo4j_connector = Neo4jConnector(settings)


@router.get("/n_ids", response_description="Get N Sub Level Entities IDs List")
async def get_n_sub_ids(category: str = None,
                        sub_level: int = 1,
                        context: str = "reality",
                        meaning: str = "literal",
                        session: Session = Depends(
                            neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_ids(category, sub_level, context, meaning)


@router.get(
    "/n_pval_corr_elems",
    response_description="Get N Sub Level P Value Correlations Elements")
async def get_n_pval_corr_elems(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_pval_corr_elems(id_list)


@router.get(
    "/n_wgt_corr_elems",
    response_description="Get N Sub Level P Weight Correlations Elements")
async def get_n_pval_corr_elems(
        id_list: Union[list[int], None] = Query(default=None),
        session: Session = Depends(neo4j_connector.get_session)):
    query_handler = Neo4jQueryHandler(session)
    return query_handler.get_sub_wgt_corr_elems(id_list)
from typing import Union, List

from fastapi import APIRouter, Depends, Query
from neo4j import Session

from app.handler.manager import Neo4jContextManager
from app.instance import neo4j_driver

router = APIRouter()


@router.get("/n/pval/corr", response_description="Get N Sub Level P Value Correlations Elements")
async def get_n_pval_corr(
        ids: Union[List[str], None] = Query(default=None),
        session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session, handler_class='querier') as neo4j_ctxt_mgr:
        try:
            query_results = neo4j_ctxt_mgr.query_pval_corr_elems(ids)
            print(f"Query executed successfully")
            return query_results
        except Exception as e:
            raise Exception(f"Error occurred while getting nodes' properties: {e}")


@router.get("/n/wgt/cov/coeff", response_description="Get N Sub Level P Value Covariance Coefficients Elements")
async def get_n_wgt_cov_co(
        ids: Union[List[str], None] = Query(default=None),
        session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session, handler_class='querier') as neo4j_ctxt_mgr:
        try:
            query_results = neo4j_ctxt_mgr.query_wgt_cov_coeff(ids)
            print(f"Query executed successfully")
            return query_results
        except Exception as e:
            raise Exception(f"Error occurred while getting nodes' properties: {e}")


@router.get("/n/wgt/cov/sdprod", response_description="Get N Sub Level P Value Covariance SD Products Elements")
async def get_n_wgt_cov_sd_pro(
        ids: Union[List[str], None] = Query(default=None),
        session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session, handler_class='querier') as neo4j_ctxt_mgr:
        try:
            query_results = neo4j_ctxt_mgr.query_wgt_cov_sdprod(ids)
            print(f"Query executed successfully")
            return query_results
        except Exception as e:
            raise Exception(f"Error occurred while getting nodes' properties: {e}")

from typing import Union, List

from fastapi import APIRouter, Depends, Query
from neo4j import Session

from app.handler.manager import Neo4jContextManager
from app.instance import neo4j_driver
from app.utils.formatter import NodeFormatter

router = APIRouter()


@router.get('/n/nodes/info', response_description="Get N Sub Level Entities IDs List")
def get_node(category: Union[str, None] = Query(default=None),
             sub_class_level: Union[str, int] = Query(default=1),
             context: Union[str, None] = Query(default='reality'),
             meaning: Union[str, None] = Query(default='literal'),
             session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session, handler_class='querier') as neo4j_ctxt_mgr:
        try:
            query_results = neo4j_ctxt_mgr.query_node_ids(category, sub_class_level, context, meaning)
            result = NodeFormatter(query_results).node_extraction('currentNode', 'parentNode', 'subLevel')
            print(f"Query executed successfully, found {len(query_results)} nodes")
            return result
        except Exception as e:
            raise Exception(f"Error occurred while getting node {category}: {e}")


@router.get("/feature", response_description="Get N Sub Level Feature")
async def get_n_sub_feature(
        ids: Union[List[str], None] = Query(default=None),
        session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session,  handler_class='querier') as neo4j_ctxt_mgr:
        try:
            query_results = neo4j_ctxt_mgr.query_props_by_id(ids)
            result = NodeFormatter(query_results).node_extraction('class')
            print(f"Query executed successfully, found {len(query_results)} nodes' feature")
            return result['class']
        except Exception as e:
            raise Exception(f"Error occurred while getting nodes' properties: {e}")


@router.get("/pvalue", response_description="Get N Sub Level P Value")
async def get_sub_n_pval(
        ids: Union[List[str], None] = Query(default=None),
        session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session, handler_class='querier') as neo4j_ctxt_mgr:
        try:
            query_results = neo4j_ctxt_mgr.query_props_by_id(ids)
            result = NodeFormatter(query_results).node_extraction('pvalue')
            print(f"Query executed successfully, found {len(query_results)} nodes' p value")
            return result['pvalue']
        except Exception as e:
            raise Exception(f"Error occurred while getting nodes' properties: {e}")


@router.get("/weight", response_description="Get N Sub Level Weight")
async def get_sub_n_wgt(
        ids: Union[List[str], None] = Query(default=None),
        session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session, handler_class='querier') as neo4j_ctxt_mgr:
        try:
            query_results = neo4j_ctxt_mgr.query_props_by_id(ids)
            result = NodeFormatter(query_results).node_extraction('weight')
            print(f"Query executed successfully, found {len(query_results)} nodes' weight")
            return result['weight']
        except Exception as e:
            raise Exception(f"Error occurred while getting nodes' properties: {e}")

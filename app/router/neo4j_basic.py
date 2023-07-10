from typing import Union, List, Dict, Any

from fastapi import APIRouter, Depends, Query, Body
from neo4j import Session

from app.handler.manager import Neo4jContextManager
from app.instance import neo4j_driver

router = APIRouter()


@router.get('/neo4j/basic', response_description="Get one node by its element id")
def get_node(node_id: Union[str, None] = Query(default=None),
             session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session) as neo4j_ctxt_mgr:
        try:
            result = neo4j_ctxt_mgr.query_node_by_id(node_id=node_id)
            return result
        except Exception as e:
            raise Exception(f"Error occurred while getting node {node_id}: {e}")


@router.post('/neo4j/basic', response_description="Create a node")
def create_node(labels: Union[List[str], None] = Body(default=None),
                properties: Union[Dict[str, Any], None] = Body(default=None),
                session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session) as neo4j_ctxt_mgr:
        try:
            node_id = neo4j_ctxt_mgr.create_node(labels=labels, properties=properties)
            return node_id
        except Exception as e:
            raise Exception(f"Error occurred while creating the node: {e}")


@router.put('/neo4j/basic', response_description="Update node's properties")
def update_node(node_id: Union[str, None] = Body(default=None),
                properties: Union[Dict[str, Any], None] = Body(default=None),
                session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session) as neo4j_ctxt_mgr:
        try:
            node = neo4j_ctxt_mgr.update_node(node_id=node_id, properties=properties)
            return node
        except Exception as e:
            raise Exception(f"Error occurred while updating the node: {e}")


@router.delete('/neo4j/basic', response_description="Delete one node by its element id")
def update_node(node_id: Union[str, None] = Query(default=None),
                session: Session = Depends(neo4j_driver.create_session)):
    with Neo4jContextManager(session=session) as neo4j_ctxt_mgr:
        try:
            neo4j_ctxt_mgr.delete_node(node_id=node_id)
            return f"Delete the node: {node_id} successfully"
        except Exception as e:
            raise Exception(f"Error occurred while deleting the node: {e}")

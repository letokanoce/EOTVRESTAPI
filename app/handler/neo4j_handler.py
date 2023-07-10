from typing import Dict, List, Any

from neo4j import Transaction

from app.cypher.delete_cypher import *
from app.cypher.query_cypher import *
from app.cypher.update_cypher import *


class Neo4jHandler:
    def __init__(self, transaction: Transaction):
        self.transaction = transaction

    def run_cypher(self, cypher: str, *args, **kwargs):
        if not cypher:
            raise ValueError("Cypher must be provided")
        try:
            result = self.transaction.run(cypher, *args, **kwargs)
            return result
        except Exception as e:
            raise Exception(f"Error occurred while running Cypher: {e}")

    def query_props_by_id(self, node_ids: List[str]):
        if not node_ids:
            raise ValueError("Node ids must be provided")
        try:
            query_result = self.run_cypher(cypher=GET_PROPS_BY_ID, node_ids=node_ids)
            result = query_result.value()
            print(f"Query executed successfully")
            return result
        except Exception as e:
            raise Exception(f"Error occurred while finding one node's properties by ID: {e}")

    def query_node_by_id(self, node_id: str):
        if not node_id:
            raise ValueError("Node id must be provided")
        try:
            query_result = self.run_cypher(cypher=GET_NODE_BY_ID, node_id=node_id)
            result = query_result.value()[0]
            print(f"Query executed successfully, found node: node {result['id']}")
            return result
        except Exception as e:
            raise Exception(f"Error occurred while finding one node by ID: {e}")

    def create_node(self, labels: List[str] = None, properties: Dict[str, Any] = None):
        if not labels and not properties:
            raise ValueError("Either labels or properties must be provided")
        try:
            query = "CREATE (n"
            if labels:
                query += ":" + ":".join(labels)

            if properties:
                query += " $props"

            query += ") RETURN elementId(n)"
            query_result = self.run_cypher(cypher=query, props=properties)
            created_node_id = query_result.single()[0]
            print(f"Node {created_node_id} created successfully")
            return created_node_id
        except Exception as e:
            raise Exception(f"Error occurred while creating the node: {e}")

    def update_node(self, node_id: str, properties: Dict[str, Any]):
        try:
            result = self.run_cypher(cypher=UPDATE_NODE_PROPS, node_id=node_id, props=properties).value()
            print(f"Node with ID {node_id} updated successfully")
            return result
        except Exception as e:
            raise Exception(f"Error occurred while updating a node: {e}")

    def delete_node(self, node_id: str):
        try:
            self.run_cypher(cypher=DELETE_NODE, node_id=node_id)
            print(f"Node with ID {node_id} deleted successfully")
        except Exception as e:
            raise Exception(f"Error occurred while deleting a node: {e}")

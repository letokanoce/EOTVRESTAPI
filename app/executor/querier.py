from typing import Union

import numpy as np

from app.cypher.query_cypher import *
from app.handler.neo4j_handler import Neo4jHandler


class QueryHandler(Neo4jHandler):
    def query_node_ids(self, category: str, sub_level: int, context: str, meaning: str):
        if not category:
            raise ValueError("The category must be provided")
        try:
            query_result = self.run_cypher(GET_NODE_IDS,
                                           {"class": category, "hop": sub_level,
                                            "context": context, "meaning": meaning}).value()
            return query_result
        except Exception as e:
            raise Exception(f"Error occurred while finding nodes: {e}")

    def query_pval_corr_elems(self, ids: Union[list[int], None] = None):
        if not ids:
            raise ValueError("Nodes id must be provided")
        try:
            coefficient_result = self.run_cypher(cypher=GET_PVAL_CORRELATION_COEFF, node_ids=ids).value()[0]
            coefficient_matrix = np.array(coefficient_result).reshape(len(ids), len(ids))
            sd_product_result = self.run_cypher(cypher=GET_PVAL_CORRELATION_SD_PROD, node_ids=ids).value()[0]
            sd_product_matrix = np.array(sd_product_result).reshape(len(ids), len(ids))
            matrix = np.multiply(coefficient_matrix, sd_product_matrix)
            query_result = list(matrix.flatten())
            return query_result
        except Exception as e:
            raise Exception(f"Error occurred while finding nodes' properties: {e}")

    def query_wgt_cov_coeff(self, ids: Union[list[int], None] = None):
        if not ids:
            raise ValueError("Nodes id must be provided")
        try:
            query_result = self.run_cypher(GET_WEIGHT_COV_COEFF, node_ids=ids).value()[0]
            return query_result
        except Exception as e:

            raise Exception(f"Error occurred while finding nodes' properties: {e}")

    def query_wgt_cov_sd_prod(self, ids: Union[list[int], None] = None):
        if not ids:
            raise ValueError("Nodes id must be provided")
        try:
            query_result = self.run_cypher(GET_WEIGHT_COV_SD_PROD, node_ids=ids).value()[0]
            return query_result
        except Exception as e:
            raise Exception(f"Error occurred while finding nodes' properties: {e}")

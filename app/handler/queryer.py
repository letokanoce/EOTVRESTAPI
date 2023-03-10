import numpy as np
from typing import Union
from neo4j import Session

from db.db_handler import Neo4jQueryer
from utils.dataproc import IProcessData
from cypher.query_cypher import *


class Neo4jQueryHandler:

    def __init__(self, session: Session, processor: IProcessData, key: str):
        self.session = session
        self.queryer = self._init_queryer(processor, key)

    def _init_queryer(self, processor: IProcessData, key: str):
        return Neo4jQueryer(self.session, processor, key)

    def query_ids(self,
                  category: str = None,
                  sub_class_level: int = 1,
                  context: str = "reality",
                  meaning: str = "literal"):
        if category:
            query_results = self.queryer.run_cypher(
                GET_N_ID, {
                    "class": category,
                    "context": context,
                    "meaning": meaning,
                    "hop": sub_class_level
                })
        else:
            query_results = []

        self.session.close()
        return query_results

    def query_feature(self, id_list: Union[list[int], None] = None):
        if id_list:
            query_results = self.queryer.run_cypher(GET_N_FEATURES,
                                                    {"id_list": id_list})
        else:
            query_results = []

        self.session.close()
        return query_results

    def query_pval_corr_elems(self, id_list: Union[list[int], None] = None):
        size = len(id_list)
        if id_list:
            query_results_1 = self.queryer.run_cypher(GET_PVAL_CORRELATIONS,
                                                      {"id_list": id_list})
            query_matrix_1 = np.array(query_results_1).reshape(size, size)
            query_results_2 = self.queryer.run_cypher(
                GET_PVAL_CORRELATIONS_PRODUCT, {"id_list": id_list})
            query_matrix_2 = np.array(query_results_2).reshape(size, size)
            matrix = np.multiply(query_matrix_1, query_matrix_2)
            query_results = list(matrix.flatten())
        else:
            query_results = []
        self.session.close()
        return query_results

    def query_wgt_cov_elems(self, id_list: Union[list[int], None] = None):
        size = len(id_list)
        if id_list:
            query_results_1 = self.queryer.run_cypher(GET_WEIGHT_CORRELATIONS,
                                                      {"id_list": id_list})
            query_matrix_1 = np.array(query_results_1).reshape(size, size)
            query_results_2 = self.queryer.run_cypher(
                GET_WEIGHT_CORRELATIONS_PRODUCT, {"id_list": id_list})
            query_matrix_2 = np.array(query_results_2).reshape(size, size)
            matrix = np.multiply(query_matrix_1, query_matrix_2)
            query_results = list(matrix.flatten())
        else:
            query_results = []
        self.session.close()
        return query_results

    def query_pval(self, id_list: Union[list[int], None] = None):
        if id_list:
            query_results = self.queryer.run_cypher(GET_N_PVALUES,
                                                    {"id_list": id_list})
        else:
            query_results = []

        self.session.close()
        return query_results

    def query_wgt(self, id_list: Union[list[int], None] = None):
        if id_list:
            query_results = self.queryer.run_cypher(GET_N_WEIGHT,
                                                    {"id_list": id_list})
        else:
            query_results = []

        self.session.close()
        return query_results

    def query_level(self,
                    parent_id: int,
                    id_list: Union[list[int], None] = None):
        if id_list:
            query_results = self.queryer.run_cypher(GET_SUB_LEVEL, {
                "id_list": id_list,
                "parent_id": parent_id
            })
        else:
            query_results = []

        self.session.close()
        return query_results
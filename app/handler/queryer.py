import numpy as np
from typing import Union
from neo4j import Session

from app.db.db_handler import Neo4jQueryer
from app.utils.data_formatter import IProcessData

from app.cypher.query_cypher import *


class Neo4jQueryHandler:

    def __init__(self, session: Session, processor: IProcessData):
        self.session = session
        self.processor = processor

    @property
    def query_session(self):
        return Neo4jQueryer(self.session, self.processor)

    def query_ids_rel(self,
                      category: str = None,
                      sub_class_level: int = 1,
                      context: str = "reality",
                      meaning: str = "literal"):
        if category:
            query_results = self.query_session.run_cypher(GET_IDS,
                                                          {"class": category, "context": context,
                                                           "meaning": meaning, "hop": sub_class_level})
        else:
            query_results = []
        self.session.close()
        return query_results

    def query_feature(self, id_list: Union[list[int], None] = None):
        if id_list:
            query_results = self.query_session.run_cypher(GET_N_FEATURES, {"id_list": id_list})
        else:
            query_results = []
        self.session.close()
        return query_results

    def query_pval(self, id_list: Union[list[int], None] = None):
        if id_list:
            query_results = self.query_session.run_cypher(GET_N_PVALUES, {"id_list": id_list})
        else:
            query_results = []
        self.session.close()
        return query_results

    def query_wgt(self, id_list: Union[list[int], None] = None):
        if id_list:
            query_results = self.query_session.run_cypher(GET_N_WEIGHT, {"id_list": id_list})
        else:
            query_results = []
        self.session.close()
        return query_results

    def query_pval_corr_elems(self, id_list: Union[list[int], None] = None):
        if id_list:
            coefficient_result = self.query_session.run_cypher(GET_PVAL_CORRELATION_CO, {"id_list": id_list})
            coefficient_matrix = np.array(coefficient_result).reshape(len(id_list), len(id_list))
            sd_product_result = self.query_session.run_cypher(GET_PVAL_CORRELATIONS_SDPRO, {"id_list": id_list})
            sd_product_matrix = np.array(sd_product_result).reshape(len(id_list), len(id_list))
            matrix = np.multiply(coefficient_matrix, sd_product_matrix)
            query_results = list(matrix.flatten())
        else:
            query_results = []
        self.session.close()
        return query_results

    def query_wgt_cov_elems(self, id_list: Union[list[int], None] = None):
        if id_list:
            coefficient_result = self.query_session.run_cypher(GET_WEIGHT_CORRELATION_CO, {"id_list": id_list})
            coefficient_matrix = np.array(coefficient_result).reshape(len(id_list), len(id_list))
            sd_product_result = self.query_session.run_cypher(GET_WEIGHT_CORRELATIONS_SDPRO, {"id_list": id_list})
            sd_product_matrix = np.array(sd_product_result).reshape(len(id_list), len(id_list))
            matrix = np.multiply(coefficient_matrix, sd_product_matrix)
            query_results = list(matrix.flatten())
        else:
            query_results = []
        self.session.close()
        return query_results

import datetime


class EnvironSettings:
    def __init__(self, context, meaning):
        self.context = context
        self.meaning = meaning


class MathLimit:
    def __init__(self, xi_0: float, gama: float, w_prime_min: float):
        self.xi_0 = xi_0
        self.gama = gama
        self.w_prime_min = w_prime_min


class BaseProfile:

    def __init__(self, category: str, sub_class_level: int, env_settings: EnvironSettings, params: dict):
        self.category = category
        self.sub_class_level = sub_class_level
        self.env_settings = env_settings
        self.node_id = params["node_id"]
        self.feature = params["feature"]
        self.p_value = params["p value"]
        self.pval_corr_mtx = params["p value correlation"]
        self.weight = params["weight"]
        self.wgt_cov_mtx = params["weight covariance"]
        self.p_hit = params["p hit"]
        self.p_fa = params["p false alarm"]
        self.num_trial = params["number of trails"]
        self.last_acc_time = datetime.datetime.now()
        self._cache = {}

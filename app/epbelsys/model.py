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
    def __init__(self, category: str, sub_level: int, env_settings: EnvironSettings):
        self.category = category
        self.sub_level = sub_level
        self.env_settings = env_settings
        self.last_acc_time = datetime.datetime.now()

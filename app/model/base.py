import datetime


class Enviroment:

    def __init__(self, context, meaning):
        self.context = context
        self.meaning = meaning


class BaseProfile:

    def __init__(self, category: str, sub_level: int, environment: Enviroment):
        self.category = category
        self.sub_level = sub_level
        self.environment = environment
        self.last_acc_time = datetime.datetime.now()

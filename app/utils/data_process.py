from abc import ABC, abstractmethod
from typing import List, Dict, Union


class IProcessData(ABC):

    @abstractmethod
    def process(self, data: any) -> Union[any, None]:
        pass


class StringProcessor(IProcessData):

    def process(self, string: str) -> Union[str, None]:
        result = ""
        for char in string:
            if char.isupper():
                result += " " + char.upper()
            else:
                result += char
        return result.lower()


class UniqOutcomesProcessor(IProcessData):

    def process(self, query_results: List[Dict],
                key: str) -> Union[list, None]:
        return list(set(d[key] for d in query_results))


class MatrixProcessor(IProcessData):

    def process(self, query_results: List[Dict],
                key: str) -> Union[list, None]:
        return [d[key] for d in query_results]
from typing import List, Dict


def convert_list_to_dict(lst: List[str]):
    result = {}
    for i in range(0, len(lst), 2):
        if i + 1 < len(lst):
            result[lst[i]] = lst[i + 1]
    return result


class NodeFormatter:
    def __init__(self, nodes: List[Dict]):
        self.nodes = nodes

    def node_extraction(self, *keys):
        result = {key: [node[key] for node in self.nodes] for key in keys}
        return result

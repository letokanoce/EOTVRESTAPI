DELETE_NODE = """
                 MATCH (n) 
                 WHERE elementId(n) = $node_id 
                 DELETE n
                 """
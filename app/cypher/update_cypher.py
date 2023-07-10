UPDATE_NODE_PROPS = """
                 MATCH (n) 
                 WHERE elementId(n) = $node_id
                 SET n += $props
                 RETURN n
             """
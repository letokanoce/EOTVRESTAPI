GET_ALL_NODES = """
       MATCH (n) 
       RETURN n
       """

GET_IDS = """
       MATCH (s {class: $class, context: $context, meaning: $meaning})
       CALL apoc.path.expandConfig(s, {
           relationshipFilter: "HAS_FEATURE",
           minLevel: 1,
           maxLevel: $hop
           }) YIELD path
       UNWIND relationships(path) AS rel
       WITH s, endNode(rel) AS subGraph, length(path) AS pathLength
       UNWIND subGraph AS node
       UNWIND pathLength AS step
       RETURN ID(s) AS parentNode, 
              collect (DISTINCT ID(node)) AS subNodes, 
              collect (step) AS subLevel
       """

GET_LEAVES_IDS = """
       MATCH (s {class: $class, context: $context, meaning: $meaning})
       CALL apoc.path.expandConfig(s, {
           relationshipFilter: "HAS_FEATURE",
           minLevel: 1,
           maxLevel: $hop
           }) YIELD path
       UNWIND relationships(path) AS rel
       WITH s,
            collect(DISTINCT endNode(rel)) AS endNodes, 
            collect(DISTINCT startNode(rel)) AS startNodes,
            length(path) AS pathLength
       UNWIND endNodes AS leaf
       WITH s, pathLength, leaf WHERE NOT leaf IN startNodes
       RETURN id(s) AS parentNode,
              collect (DISTINCT ID(leaf)) AS subNodes,
              collect (pathLength) AS subLevel
       """

GET_N_FEATURES = """
       MATCH (n)
       WHERE id(n) in $id_list
       RETURN collect(n.class) AS features
       """

GET_N_PVALUES = """
       MATCH (n)
       WHERE id(n) in $id_list
       RETURN collect(n.pvalue) AS features
       """

GET_N_WEIGHT = """
       MATCH (n)
       WHERE id(n) in $id_list
       RETURN collect(n.weight) AS features
       """
GET_PVAL_CORRELATION_CO = """
       UNWIND $id_list AS x
       UNWIND $id_list AS y
       OPTIONAL MATCH (a)-[r:CORRELATE_WITH]-(b)
       WHERE ID(a) = x AND ID(b) = y 
       RETURN collect(coalesce(r.pval_correlation, 1)) AS CoefficientMatrix
       """

GET_PVAL_CORRELATIONS_SDPRO = """
       UNWIND $id_list AS x
       UNWIND $id_list AS y
       MATCH (a),(b)
       WHERE id(a) = x AND id(b) =y
       RETURN collect((a.pval_sd * b.pval_sd)) AS SdProduct
       """

GET_WEIGHT_CORRELATION_CO = """
       UNWIND $id_list AS x
       UNWIND $id_list AS y
       OPTIONAL MATCH (n1)-[r:CORRELATE_WITH]-(n2)
       WHERE id(n1) = x AND id(n2) = y AND x <> y
       WITH x, y,
         CASE
           WHEN x = y THEN 1
           WHEN r IS NULL THEN 10
           ELSE r.weight_correlation
         END AS correlation
       RETURN collect(correlation) AS CoefficientMatrix
       """

GET_WEIGHT_CORRELATIONS_SDPRO = """
       UNWIND $id_list AS x
       UNWIND $id_list AS y
       MATCH (a),(b)
       WHERE id(a) = x AND id(b) =y
       RETURN collect((a.weight_sd * b.weight_sd)) AS SdProduct
       """

# GET_N_ID = """
#        MATCH (s {class: $class, context: $context, meaning: $meaning})
#        OPTIONAL MATCH p = (s)-[:HAS_FEATURE*]->()
#        CALL apoc.path.expandConfig(s, {
#               relationshipFilter: "HAS_FEATURE",
#               minLevel: 1,
#               maxLevel: $hop
#               })
#        YIELD path
#        UNWIND relationShips(path) AS rel
#        WITH collect(DISTINCT endNode(rel)) AS endNodes,
#        collect(DISTINCT startNode(rel)) AS startNodes,s,p
#        UNWIND endNodes AS leaf
#        WITH leaf, s, p WHERE NOT leaf IN startNodes
#        RETURN [collect(DISTINCT id(leaf)), id(s), max(length(p))] AS r
#        """
#
# GET_PARENT_NODE = """
#        WITH id_list AS id
#        UNWIND id AS x
#        MATCH (a)-[r:HAS_FEATURE]->(b)
#        WHERE id(b) = x
#        RETURN id(a)
#        """
#
# GET_SUB_LEVEL = """
#       WITH $id_list AS id
#       MATCH (n)
#       WHERE ID(n) = $parent_id
#       UNWIND id AS i
#       MATCH (m)
#       WHERE ID(m) = i
#       WITH n, m
#       MATCH p = shortestPath((n)-[:HAS_FEATURE*]-(m))
#       RETURN [collect(length(p)), '1'] AS r
#       """

GET_FEATURES = """
       MATCH (c {class: $class, context: $context, meaning: $meaning}) 
       RETURN c.features AS r;
       """

GET_ALL_NODES = """
       MATCH (n) 
       RETURN n;"""

GET_N_ID = """
       MATCH (s {class: $class, context: $context, meaning: $meaning})
       OPTIONAL MATCH p = (s)-[:HAS_FEATURE*]->()
       CALL apoc.path.expandConfig(s, {
              relationshipFilter: "HAS_FEATURE",
              minLevel: 1,
              maxLevel: $hop
              })
       YIELD path
       UNWIND relationShips(path) AS rel
       WITH collect(DISTINCT endNode(rel)) AS endNodes, 
       collect(DISTINCT startNode(rel)) AS startNodes,s,p
       UNWIND endNodes AS leaf
       WITH leaf, s, p WHERE NOT leaf IN startNodes
       RETURN [collect(DISTINCT id(leaf)), id(s), max(length(p))] AS r
       """

GET_N_FEATURES = """
       WITH $id_list AS id
       UNWIND id AS i
       MATCH (n)
       WHERE id(n) = i
       RETURN n.class AS r
       """

GET_N_PVALUES = """
       WITH $id_list AS id
       UNWIND id AS i
       MATCH (n)
       WHERE id(n) = i
       RETURN n.pvalue AS r
       """
GET_N_WEIGHT = """
       WITH $id_list AS id
       UNWIND id AS i
       MATCH (n)
       WHERE id(n) = i
       RETURN n.weight AS r
       """

GET_N_PVAL_SD = """
       WITH $id_list AS id
       UNWIND id AS i
       MATCH (n)
       WHERE id(n) = i
       RETURN n.pval_sd AS r
       """

GET_N_WEIGHT_SD = """
       WITH $id_list AS id
       UNWIND id AS i
       MATCH (n)
       WHERE id(n) = i
       RETURN n.weight_sd AS r
       """

GET_PVAL_CORRELATIONS = """
       WITH $id_list AS id_1, $id_list AS id_2
       UNWIND id_1 AS x
       UNWIND id_2 AS y
       OPTIONAL MATCH (a)-[r:CORRELATE_WITH]-(b)
       WHERE ID(a) = x AND ID(b) = y 
       RETURN COALESCE(r.pval_correlation, 1) AS r
       """

GET_WEIGHT_CORRELATIONS = """
       WITH $id_list AS id_1, $id_list AS id_2
       UNWIND id_1 AS x
       UNWIND id_2 AS y
       OPTIONAL MATCH (a)-[r:CORRELATE_WITH]-(b)
       WHERE ID(a) = x AND ID(b) = y 
       RETURN COALESCE(r.weight_correlation, 100000) AS r
       """

GET_PVAL_CORRELATIONS_PRODUCT = """
       WITH $id_list AS id_1, $id_list AS id_2
       UNWIND id_1 AS x
       UNWIND id_2 AS y
       MATCH (a),(b)
       WHERE ID(a) = x AND ID(b) =y
       RETURN (a.pval_sd * b.pval_sd) AS r
       """

GET_WEIGHT_CORRELATIONS_PRODUCT = """
       WITH $id_list AS id_1, $id_list AS id_2
       UNWIND id_1 AS x
       UNWIND id_2 AS y
       MATCH (a),(b)
       WHERE ID(a) = x AND ID(b) =y
       RETURN (a.weight_sd * b.weight_sd) AS r
       """

GET_PARENT_NODE = """
       WITH id_list AS id
       UNWIND id AS x
       MATCH (a)-[r:HAS_FEATURE]->(b)
       WHERE id(b) = x
       RETURN id(a)
       """

GET_SUB_LEVEL = """
      WITH $id_list AS id
      MATCH (n {class: $class, context: $context, meaning: $meaning}) 
      UNWIND id AS i
      MATCH (m) 
      WHERE ID(m) = i
      WITH n, m
      MATCH p = shortestPath((n)-[:HAS_FEATURE*]-(m))
      RETURN length(p) AS r
      """
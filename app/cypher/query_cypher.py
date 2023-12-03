GET_NODE_BY_ID = """
                    MATCH (n) 
                    WHERE elementId(n) = $node_id 
                    RETURN {id: elementId(n), labels: labels(n), properties: properties(n)} AS node
                    """

GET_PROPS_BY_ID = """
                     MATCH (n)
                     WHERE elementId(n) IN $node_ids
                     RETURN properties(n) AS properties
                     """

GET_NODE_IDS = """
       MATCH (s {class: $class, context: $context, meaning: $meaning})
       CALL apoc.path.expandConfig(s, {
            relationshipFilter: "HAS_FEATURE",
            minLevel: 1,
            maxLevel: $hop
            }) YIELD path
        RETURN {parentNode:elementId(s), currentNode: elementId(last(nodes(path))), subLevel: length(path)} AS node
        """

GET_PVAL_CORRELATION_COEFF = """
       UNWIND $node_ids AS x
       UNWIND $node_ids AS y
       OPTIONAL MATCH (a)-[r:CORRELATE_WITH]-(b)
       WHERE elementId(a) = x AND elementId(b) = y 
       RETURN collect(coalesce(r.pval_corr, 1)) AS CoefficientMatrix
       """

GET_PVAL_CORRELATION_SD_PROD = """
       UNWIND $node_ids AS x
       UNWIND $node_ids AS y
       MATCH (a),(b)
       WHERE elementId(a) = x AND elementId(b) =y
       RETURN collect((a.pval_sd * b.pval_sd)) AS SdProduct
       """

GET_WEIGHT_COV_COEFF = """
       UNWIND $node_ids AS x
       UNWIND $node_ids AS y
       OPTIONAL MATCH (n1)-[r:CORRELATE_WITH]-(n2)
       WHERE elementId(n1) = x AND elementId(n2) = y AND x <> y
       WITH x, y,
         CASE
           WHEN x = y THEN 1
           WHEN r IS NULL THEN 10
           ELSE r.wgt_corr
         END AS correlation
       RETURN collect(correlation) AS CoefficientMatrix
       """

GET_WEIGHT_COV_SD_PROD = """
       UNWIND $node_ids AS x
       UNWIND $node_ids AS y
       MATCH (a),(b)
       WHERE elementId(a) = x AND elementId(b) =y
       RETURN collect((a.wgt_sd * b.wgt_sd)) AS SdProduct
       """

data = [
    {
        "id": "4:8da76954-3af3-4496-98c0-d7fe103e0ce4:0",
        "properties": {
            "namae": "Yoritomo",
            "uji": "Minamoto",
            "force": "Bakufu",
            "class": "Shogun"
        },
        "labels": [
            "Person"
        ]
    },
    {
        "id": "4:8da76954-3af3-4496-98c0-d7fe103e0ce4:2",
        "properties": {
            "namae": "Noriyori",
            "uji": "Minamoto",
            "force": "Bakufu",
            "class": "Mikawa-no-kami"
        },
        "labels": [
            "Person"
        ]
    }
]

NEW_NODE = """
        WITH $add_params AS params
        MERGE (n {class: $class, context: $context, meaning: $meaning})
        SET n += params
        RETURN n
        """

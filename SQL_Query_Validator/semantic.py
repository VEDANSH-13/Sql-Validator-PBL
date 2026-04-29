from schema import SCHEMA

def semantic_check(parsed_query):

    if parsed_query["type"] == "SELECT":
        table = parsed_query["table"]
        columns = parsed_query["columns"]
        condition = parsed_query["condition"]

        if table not in SCHEMA:
            raise Exception(f"Table '{table}' does not exist")

        if columns != ["*"]:
            for col in columns:
                if col not in SCHEMA[table]:
                    raise Exception(f"Column '{col}' does not exist in table '{table}'")

        if condition:
            if condition["column"] not in SCHEMA[table]:
                raise Exception(f"Column '{condition['column']}' does not exist in table '{table}'")

    elif parsed_query["type"] == "INSERT":
        table = parsed_query["table"]
        values = parsed_query["values"]

        if table not in SCHEMA:
            raise Exception(f"Table '{table}' does not exist")

        if len(values) != len(SCHEMA[table]):
            raise Exception("Number of values does not match table columns")

    elif parsed_query["type"] == "UPDATE":
        table = parsed_query["table"]
        set_column = parsed_query["set_column"]
        condition = parsed_query["condition"]

        if table not in SCHEMA:
            raise Exception(f"Table '{table}' does not exist")

        if set_column not in SCHEMA[table]:
            raise Exception(f"Column '{set_column}' does not exist in table '{table}'")

        if condition:
            if condition["column"] not in SCHEMA[table]:
                raise Exception(f"Column '{condition['column']}' does not exist in table '{table}'")

    elif parsed_query["type"] == "DELETE":
        table = parsed_query["table"]
        condition = parsed_query["condition"]

        if table not in SCHEMA:
            raise Exception(f"Table '{table}' does not exist")

        if condition:
            if condition["column"] not in SCHEMA[table]:
                raise Exception(f"Column '{condition['column']}' does not exist in table '{table}'")

    return "Semantic validation successful"
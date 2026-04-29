class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type=None, value=None):
        token = self.current()
        if token is None:
            raise Exception("Unexpected end of query")

        if token_type and token[0] != token_type:
            raise Exception(f"Expected {token_type}, got {token}")

        if value and token[1].upper() != value:
            raise Exception(f"Expected {value}, got {token}")
        self.pos += 1
        return token

    def parse(self):
        token = self.current()
        if token[1].upper() == "SELECT":
            return self.select_stmt()

        elif token[1].upper() == "INSERT":
            return self.insert_stmt()

        elif token[1].upper() == "UPDATE":
            return self.update_stmt()

        elif token[1].upper() == "DELETE":
            return self.delete_stmt()

        else:
            raise Exception("Unsupported query type")

    def select_stmt(self):
        self.eat("KEYWORD", "SELECT")
        columns = self.select_list()

        self.eat("KEYWORD", "FROM")
        table = self.table_name()

        condition = None
        if self.current() and self.current()[1].upper() == "WHERE":
            condition = self.where_clause()

        return {
            "type": "SELECT",
            "columns": columns,
            "table": table,
            "condition": condition
        }
    def select_list(self):
        token = self.current()

        if token[1] == "*":
            self.eat("SYMBOL", "*")
            return ["*"]

        columns = [self.column()]

        while self.current() and self.current()[1] == ",":
            self.eat("SYMBOL", ",")
            columns.append(self.column())

        return columns

    def column(self):
        token = self.current()

        if token[0] == "IDENTIFIER":
            return self.eat("IDENTIFIER")[1]
        else:
            raise Exception("Invalid column name")

    def table_name(self):
        token = self.current()

        if token[0] == "IDENTIFIER":
            return self.eat("IDENTIFIER")[1]
        else:
            raise Exception("Invalid table name")

    def where_clause(self):
        self.eat("KEYWORD", "WHERE")

        column = self.column()
        operator = self.eat("OPERATOR")[1]
        value = self.value()

        return {
            "column": column,
            "operator": operator,
            "value": value
        }

    def value(self):
        token = self.current()

        if token[0] in ["NUMBER", "STRING", "IDENTIFIER"]:
            return self.eat(token[0])[1]
        else:
            raise Exception("Invalid value in WHERE clause")

    def insert_stmt(self):
        self.eat("KEYWORD", "INSERT")
        self.eat("KEYWORD", "INTO")

        table = self.table_name()

        self.eat("KEYWORD", "VALUES")
        values = self.values_list()

        return {
            "type": "INSERT",
            "table": table,
            "values": values
        }

    def values_list(self):
        values = []

        self.eat("SYMBOL", "(")

        values.append(self.value())

        while self.current() and self.current()[1] == ",":
            self.eat("SYMBOL", ",")
            values.append(self.value())

        self.eat("SYMBOL", ")")

        return values

    def update_stmt(self):
        self.eat("KEYWORD", "UPDATE")
        table = self.table_name()

        self.eat("KEYWORD", "SET")
        set_column = self.column()
        self.eat("OPERATOR", "=")
        set_value = self.value()

        condition = None
        if self.current() and self.current()[1].upper() == "WHERE":
            condition = self.where_clause()

        return {
            "type": "UPDATE",
            "table": table,
            "set_column": set_column,
            "set_value": set_value,
            "condition": condition
        }

    def delete_stmt(self):
        self.eat("KEYWORD", "DELETE")
        self.eat("KEYWORD", "FROM")
        table = self.table_name()

        condition = None
        if self.current() and self.current()[1].upper() == "WHERE":
            condition = self.where_clause()

        return {
            "type": "DELETE",
            "table": table,
            "condition": condition
        }

    
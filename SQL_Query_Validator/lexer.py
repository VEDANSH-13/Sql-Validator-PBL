import re

KEYWORDS = {
    "SELECT", "FROM", "WHERE",
    "INSERT", "INTO", "VALUES",
    "UPDATE", "SET",
    "DELETE",
    "INNER", "LEFT", "RIGHT", "FULL",
    "NATURAL", "CROSS", "JOIN", "ON"
}

OPERATORS = {"=", ">", "<", ">=", "<=", "!="}
SYMBOLS = {",", ";", "(", ")", ".", "*"}


def tokenize(query):
    pattern = r"'[^']*'|>=|<=|!=|=|>|<|[(),;.*]|[A-Za-z_][A-Za-z0-9_]*|\d+"

    parts = re.findall(pattern, query)
    tokens = []

    for part in parts:
        upper_part = part.upper()

        if upper_part in KEYWORDS:
            tokens.append(("KEYWORD", upper_part))
        elif part in OPERATORS:
            tokens.append(("OPERATOR", part))
        elif part in SYMBOLS:
            tokens.append(("SYMBOL", part))
        elif re.fullmatch(r"\d+", part):
            tokens.append(("NUMBER", part))
        elif re.fullmatch(r"'[^']*'", part):
            tokens.append(("STRING", part))
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part):
            tokens.append(("IDENTIFIER", part))
        else:
            tokens.append(("INVALID", part))

    return tokens
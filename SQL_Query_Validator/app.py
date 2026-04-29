from flask import Flask, render_template, request
from collections import deque
from lexer import tokenize
from parser import Parser
from semantic import semantic_check

app = Flask(__name__)

query_history = deque(maxlen=5)


def generate_suggestion(query, error_msg):
    query = query.strip()

    if "FROM" in error_msg and query.upper().startswith("SELECT"):
        return "Suggestion: Add the FROM keyword after the selected columns."

    if "INTO" in error_msg and query.upper().startswith("INSERT"):
        return "Suggestion: INSERT queries should include the INTO keyword."

    if "Table" in error_msg and "does not exist" in error_msg:
        return "Suggestion: Check whether the table name matches the predefined schema."

    if "Column" in error_msg and "does not exist" in error_msg:
        return "Suggestion: Verify the column name according to the table schema."

    if "Unexpected end of query" in error_msg:
        return "Suggestion: The query seems incomplete. Check for missing values, keywords, or conditions."

    if "Expected" in error_msg:
        return "Suggestion: Check the order of keywords and symbols in the query."

    return "Suggestion: Review the SQL syntax and schema details."


def highlight_error(query, error_msg):
    pointer_line = ""

    if "Column '" in error_msg:
        start = error_msg.find("Column '") + len("Column '")
        end = error_msg.find("'", start)
        wrong_col = error_msg[start:end]
        pos = query.lower().find(wrong_col.lower())
        if pos != -1:
            pointer_line = " " * pos + "^"

    elif "Table '" in error_msg:
        start = error_msg.find("Table '") + len("Table '")
        end = error_msg.find("'", start)
        wrong_table = error_msg[start:end]
        pos = query.lower().find(wrong_table.lower())
        if pos != -1:
            pointer_line = " " * pos + "^"

    elif "FROM" in error_msg:
        pos = len(query)
        pointer_line = " " * pos + "^"

    elif "INTO" in error_msg:
        pos = len("INSERT ")
        pointer_line = " " * pos + "^"

    if pointer_line:
        return query + "\n" + pointer_line

    return query


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    tokens = []
    suggestion = ""
    highlighted_query = ""
    current_query = ""

    if request.method == "POST":
        current_query = request.form["query"]

        try:
            tokens = tokenize(current_query)

            parser = Parser(tokens)
            parsed_query = parser.parse()

            semantic_check(parsed_query)

            result = "Query is valid"

            query_history.appendleft({
                "query": current_query,
                "status": "Valid"
            })

        except Exception as e:
            error_msg = str(e)
            result = "Error: " + error_msg
            suggestion = generate_suggestion(current_query, error_msg)
            highlighted_query = highlight_error(current_query, error_msg)

            query_history.appendleft({
                "query": current_query,
                "status": "Error"
            })

    return render_template(
        "index.html",
        result=result,
        tokens=tokens,
        suggestion=suggestion,
        highlighted_query=highlighted_query,
        history=list(query_history),
        current_query=current_query
    )


if __name__ == "__main__":
    app.run(debug=True)
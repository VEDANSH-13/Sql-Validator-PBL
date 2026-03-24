# Sql-Validator-PBL
# Mini SQL Query Validator

This project implements a basic SQL query validator using compiler design principles.

## Features
- Lexical Analysis using Flex
- Syntax Analysis using Bison
- Supports:
  - SELECT
  - INSERT
  - UPDATE
  - DELETE
- Error handling for invalid tokens and syntax errors

## How to Run

```bash
lex sql.l
yacc -d sql.y
gcc lex.yy.c y.tab.c -o sql_validator
./sql_validator

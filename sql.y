%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *s);
int yylex();
extern FILE *yyin;
extern char *yytext;
%}

%token SELECT FROM WHERE INSERT INTO VALUES
%token UPDATE DELETE SET
%token IDENTIFIER NUMBER
%token COMMA SEMICOLON EQUALS
%token LPAREN RPAREN

%%

query:
      select_stmt SEMICOLON   { printf("Valid SELECT query\n"); }
    | insert_stmt SEMICOLON   { printf("Valid INSERT query\n"); }
    | update_stmt SEMICOLON   { printf("Valid UPDATE query\n"); }
    | delete_stmt SEMICOLON   { printf("Valid DELETE query\n"); }
    ;

select_stmt:
      SELECT IDENTIFIER FROM IDENTIFIER
    | SELECT IDENTIFIER FROM IDENTIFIER WHERE IDENTIFIER EQUALS NUMBER
    ;

insert_stmt:
      INSERT INTO IDENTIFIER VALUES LPAREN NUMBER RPAREN
    ;

update_stmt:
      UPDATE IDENTIFIER SET IDENTIFIER EQUALS NUMBER
    ;

delete_stmt:
      DELETE FROM IDENTIFIER
    ;

%%

void yyerror(const char *s) {
    printf("Syntax Error: %s near '%s'\n", s, yytext);
}

int main() {
    FILE *file = fopen("input.sql", "r");
    if (!file) {
        printf("Error opening file\n");
        return 1;
    }

    yyin = file;
    yyparse();

    fclose(file);
    return 0;
}

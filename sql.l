%{
#include "y.tab.h"
#include <stdio.h>
%}

%%
"SELECT"        { return SELECT; }
"FROM"          { return FROM; }
"WHERE"         { return WHERE; }
"INSERT"        { return INSERT; }
"INTO"          { return INTO; }
"VALUES"        { return VALUES; }
"UPDATE"        { return UPDATE; }
"DELETE"        { return DELETE; }
"SET"           { return SET; }

[a-zA-Z_][a-zA-Z0-9_]*   { return IDENTIFIER; }
[0-9]+                   { return NUMBER; }

","     { return COMMA; }
";"     { return SEMICOLON; }
"="     { return EQUALS; }
"("     { return LPAREN; }
")"     { return RPAREN; }

[ \t\n]+    ;   // ignore whitespace
.           { printf("Invalid token: %s\n", yytext); }
%%

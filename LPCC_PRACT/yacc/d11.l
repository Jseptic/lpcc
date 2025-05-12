%{
#include "sincos.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
"sin"           { return SIN; }
"cos"           { return COS; }
[0-9]+(\.[0-9]+)?   { yylval.dval = atof(yytext); return NUMBER; }
[a-zA-Z][a-zA-Z0-9]* { yylval.sval = strdup(yytext); return IDENTIFIER; }
"="             { return '='; }
"("             { return '('; }
")"             { return ')'; }
[+\-*/]        { return yytext[0]; }
[\n]           { return '\n'; }
[ \t]+         { /* Ignore whitespace */ }
.              { /* Ignore any unexpected character */ }
%%

int yywrap(void) {
    return 1;
}
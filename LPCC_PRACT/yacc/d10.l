%{
#include "expr.tab.h"
#include <stdlib.h>
%}

%%
[0-9]+(\.[0-9]+)?   { yylval.dval = atof(yytext); return NUMBER; }
[ \t\n]+            { /* Ignore whitespace */ }
.                   { return yytext[0]; }
%%

int yywrap(void) {
    return 1;
}
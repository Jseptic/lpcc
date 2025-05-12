%{
#include "b10.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
[a-zA-Z][a-zA-Z0-9_]*  {
                           yylval.str = strdup(yytext);
                           return IDENTIFIER;
                        }
"-"                    { return '-'; }
[\n]+                  { return '\n'; }
[ \t]+                 { /* Ignore whitespace */ }
.                      { /* Ignore any other character */ }
%%

int yywrap(void) {
    return 1;
}
%{
#include "bvar.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
[a-zA-Z][a-zA-Z0-9_]*   { 
                            /* Make a dynamically allocated copy of the identifier */
                            yylval.id = strdup(yytext);
                            return IDENTIFIER; 
                         }
[\n]+                   { return '\n'; }
[ \t]+                  { /* Ignore whitespace */ }
.                       { printf("Invalid character: %s\n", yytext); }
%%

int yywrap(void) {
    return 1;
}
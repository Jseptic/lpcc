%{
#include "d11.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
"pow"           { return POW; }
"log"           { return LOG; }
[a-zA-Z][a-zA-Z0-9_]* { 
                        yylval.sval = strdup(yytext); 
                        return IDENTIFIER; 
                  }
[0-9]+(\.[0-9]+)?  { yylval.dval = atof(yytext); return NUMBER; }
"="             { return '='; }
","             { return ','; }
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
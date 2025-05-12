%{
#include "b11.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
"sqrt"               { return SQRT; }
"strlen"             { return STRLEN; }
[a-zA-Z][a-zA-Z0-9_]* { 
                        /* Return IDENTIFIER.
                           This rule is placed after "sqrt" and "strlen",
                           so that these keywords get recognized first. */
                        yylval.sval = strdup(yytext);
                        return IDENTIFIER;
                     }
[0-9]+(\.[0-9]+)?    { yylval.dval = atof(yytext); return NUMBER; }
\"([^"\n]|\\")*\"    { 
                        /* Remove the surrounding quotes */
                        int len = strlen(yytext);
                        char *s = (char *)malloc(len - 1);
                        strncpy(s, yytext+1, len-2);
                        s[len-2] = '\0';
                        yylval.sval = s;
                        return STRING;
                    }
"="                 { return '='; }
"("                 { return '('; }
")"                 { return ')'; }
[ \t\n]+           { /* Ignore whitespace */ }
.                   { /* Ignore any unexpected characters */ }
%%

int yywrap(void) {
    return 1;
}
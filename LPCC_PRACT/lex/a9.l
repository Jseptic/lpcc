%{
#include <stdio.h>
%}

/* Define simple token rules for a C program */
%%
"int"                        { printf("%s : Keyword\n", yytext); }
[_a-zA-Z][_a-zA-Z0-9]*        { printf("%s : Identifier\n", yytext); }
[0-9]+                       { printf("%s : Number\n", yytext); }
"="                          { printf("%s : Assignment Operator\n", yytext); }
"-"                          { printf("%s : Minus Operator\n", yytext); }
";"                          { printf("%s : Semicolon\n", yytext); }
","                          { printf("%s : Comma\n", yytext); }
"{"                          { printf("%s : Left Brace\n", yytext); }
"}"                          { printf("%s : Right Brace\n", yytext); }
[ \t\n]+                     { /* Ignore whitespace */ }
.                            { printf("%s : Unknown token\n", yytext); }
%%

int main(void)
{
    yylex();
    return 0;
}
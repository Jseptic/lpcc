%{
#include <stdio.h>
%}

%%
"{"                           { printf("%s : Left Brace\n", yytext); }
"}"                           { printf("%s : Right Brace\n", yytext); }
"char"                        { printf("%s : Keyword (char)\n", yytext); }
"printf"                      { printf("%s : Identifier (printf)\n", yytext); }
"("                           { printf("%s : Left Parenthesis\n", yytext); }
")"                           { printf("%s : Right Parenthesis\n", yytext); }
"="                           { printf("%s : Assignment Operator\n", yytext); }
";"                           { printf("%s : Semicolon\n", yytext); }
\"(\\.|[^"])*\"               { printf("%s : String Literal\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*         { printf("%s : Identifier\n", yytext); }
[0-9]+                        { printf("%s : Number\n", yytext); }
[ \t\n]+                     { /* Ignore whitespace */ }
.                             { printf("%s : Unknown token\n", yytext); }
%%

int main(void) {
    yylex();
    return 0;
}
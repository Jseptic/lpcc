%{
#include <stdio.h>
#include <string.h>
%}

/* Definitions:
   This lexer recognizes a few select words from the sample input 
   and prints out the corresponding part-of-speech.
*/

%%
[Dd]read         { printf("%s : Verb/Adjective\n", yytext); }
[itI][tT]       { printf("%s : Pronoun\n", yytext); }
[Rr]un          { printf("%s : Verb\n", yytext); }
from            { printf("%s : Preposition\n", yytext); }
[Dd]estiny      { printf("%s : Noun\n", yytext); }
[arrivesA][rR][rR][iI][vV][eE][sS] { printf("%s : Verb\n", yytext); }
all             { printf("%s : Adverb\n", yytext); }
the             { printf("%s : Determiner\n", yytext); }
same            { printf("%s : Adjective/Adverb\n", yytext); }
[.,;:!?]       { printf("%s : Punctuation\n", yytext); }
[ \t\n]+       { /* Ignore whitespace */ }
.               { printf("%s : Unknown\n", yytext); }
%%

int main(void) {
    yylex();
    return 0;
}
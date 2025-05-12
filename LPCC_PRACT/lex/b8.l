%{
#include <stdio.h>
#include <string.h>
%}

%%

[Hh]ello           { printf("%s : Interjection\n", yytext); }
[Hh]ow             { printf("%s : Interrogative Adverb\n", yytext); }
are                { printf("%s : Verb\n", yytext); }
[Yy]ou             { printf("%s : Pronoun\n", yytext); }
[Ii]['’]m          { printf("%s : Contraction (I am)\n", yytext); }
[fF]ine            { printf("%s : Adjective\n", yytext); }
[Tt]hank           { printf("%s : Interjection\n", yytext); }
[.,;:!?]           { printf("%s : Punctuation\n", yytext); }
[ \t\n]+           { /* Ignore whitespace */ }
.                  { printf("%s : Unknown\n", yytext); }

%%

int main(void) {
    yylex();
    return 0;
}
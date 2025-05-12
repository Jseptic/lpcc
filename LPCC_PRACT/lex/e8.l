%{
#include <stdio.h>
%}

%%
[Ee]very              { printf("%s : Determiner\n", yytext); }
[gG]eneration         { printf("%s : Noun\n", yytext); }
[Ii]magines           { printf("%s : Verb\n", yytext); }
[itI]tself            { printf("%s : Reflexive Pronoun\n", yytext); }
to                    { printf("%s : Preposition/Infinitive Marker\n", yytext); }
be                    { printf("%s : Verb\n", yytext); }
[mM]ore               { printf("%s : Adverb\n", yytext); }
[Ii]ntelligent        { printf("%s : Adjective\n", yytext); }
than                  { printf("%s : Comparative Marker\n", yytext); }
[Tt]he                { printf("%s : Determiner\n", yytext); }
[Oo]ne                { printf("%s : Noun\n", yytext); }
[Tt]hat               { printf("%s : Demonstrative Pronoun\n", yytext); }
[Ww]ent              { printf("%s : Verb (Past Tense)\n", yytext); }
[bB]efore             { printf("%s : Preposition\n", yytext); }
[Ii]t                 { printf("%s : Pronoun\n", yytext); }
,                     { printf("%s : Punctuation\n", yytext); }
[aA]nd               { printf("%s : Conjunction\n", yytext); }
[wW]iser             { printf("%s : Adjective\n", yytext); }
[Cc]omes              { printf("%s : Verb\n", yytext); }
[aA]fter              { printf("%s : Preposition\n", yytext); }
[.,;:!?]             { printf("%s : Punctuation\n", yytext); }
[ \t\n]+             { /* Ignore whitespace */ }
.                     { printf("%s : Unknown\n", yytext); }
%%

int main(void) {
    yylex();
    return 0;
}
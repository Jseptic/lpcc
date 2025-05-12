%{
#include <stdio.h>
%}

%%
[Hh]uman                    { printf("%s : Noun\n", yytext); }
[Bb]eings                   { printf("%s : Noun\n", yytext); }
[hH]ave                     { printf("%s : Verb\n", yytext); }
[[:<:]][Aa][[:>:]]          { printf("%s : Determiner\n", yytext); }
[Ss]trong                   { printf("%s : Adjective\n", yytext); }
[Dd]ramatic                 { printf("%s : Adjective\n", yytext); }
[Ii]nstinct                 { printf("%s : Noun\n", yytext); }
[Tt]oward                   { printf("%s : Preposition\n", yytext); }
[Bb]inary                  { printf("%s : Adjective\n", yytext); }
[Tt]hinking                { printf("%s : Noun (Gerund)\n", yytext); }
[.,;:!?]                   { printf("%s : Punctuation\n", yytext); }
[[:<:]][Aa][[:>:]]          { printf("%s : Determiner\n", yytext); }
[Bb]asic                   { printf("%s : Adjective\n", yytext); }
[Uu]rge                    { printf("%s : Noun\n", yytext); }
[[:<:]][Tt][Oo][[:>:]]       { printf("%s : Preposition/Infinitive Marker\n", yytext); }
[Dd]ivide                  { printf("%s : Verb\n", yytext); }
[Tt]hings                  { printf("%s : Noun\n", yytext); }
[Ii]nto                    { printf("%s : Preposition\n", yytext); }
[[:<:]][Tt][Ww][Oo][[:>:]]   { printf("%s : Numeral\n", yytext); }
[Dd]istinct                { printf("%s : Adjective\n", yytext); }
[Gg]roups                  { printf("%s : Noun\n", yytext); }
[Ww]ith                    { printf("%s : Preposition\n", yytext); }
[Nn]othing                 { printf("%s : Pronoun\n", yytext); }
[Bb]ut                     { printf("%s : Conjunction\n", yytext); }
[[:<:]][Aa][Nn][[:>:]]      { printf("%s : Determiner\n", yytext); }
[Ee]mpty                   { printf("%s : Adjective\n", yytext); }
[Gg]ap                     { printf("%s : Noun\n", yytext); }
[Ii]n                      { printf("%s : Preposition\n", yytext); }
[Bb]etween                 { printf("%s : Preposition/Adverb\n", yytext); }
[ \t\n]+                   { /* Ignore whitespace */ }
.                          { printf("%s : Unknown\n", yytext); }
%%

int main(void) {
    yylex();
    return 0;
}
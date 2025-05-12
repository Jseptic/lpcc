%{
#include <stdio.h>
%}

%%
[Ii]f                   { printf("%s : Conjunction\n", yytext); }
[Yy]ou                  { printf("%s : Pronoun\n", yytext); }
[Nn]ever                { printf("%s : Adverb\n", yytext); }
[Ll]ight                { printf("%s : Verb\n", yytext); }
[Tt]he                 { printf("%s : Determiner\n", yytext); }
[cC]igarette            { printf("%s : Noun\n", yytext); }
[,]                    { printf("%s : Punctuation\n", yytext); }
[Yy]ou                  { printf("%s : Pronoun\n", yytext); }
[Gg]ive                { printf("%s : Verb\n", yytext); }
[Tt]he                 { printf("%s : Determiner\n", yytext); }
[Tt]hing               { printf("%s : Noun\n", yytext); }
[Tt]hat                { printf("%s : Pronoun/Determiner\n", yytext); }
[Cc]an                 { printf("%s : Modal Verb\n", yytext); }
[Kk]ill                { printf("%s : Verb\n", yytext); }
[Yy]ou                  { printf("%s : Pronoun\n", yytext); }
[Tt]he                 { printf("%s : Determiner\n", yytext); }
[Pp]ower               { printf("%s : Noun\n", yytext); }
[Ii]t                  { printf("%s : Pronoun\n", yytext); }
[Nn]eeds               { printf("%s : Verb\n", yytext); }
[Tt]o                  { printf("%s : Preposition/Infinitive Marker\n", yytext); }
[ \t\n]+               { /* ignore whitespace */ }
.                      { printf("%s : Unknown\n", yytext); }
%%

int main(void) {
    yylex();
    return 0;
}
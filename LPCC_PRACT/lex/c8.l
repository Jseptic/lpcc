%{
#include <stdio.h>
%}

%%
[Tt]he                { printf("%s : Determiner\n", yytext); }
[Ii]mportant           { printf("%s : Adjective\n", yytext); }
[Tt]hing              { printf("%s : Noun\n", yytext); }
is                    { printf("%s : Verb\n", yytext); }
to                    { printf("%s : Preposition/Infinitive Marker\n", yytext); }
not                   { printf("%s : Adverb\n", yytext); }
stop                  { printf("%s : Verb\n", yytext); }
questioning           { printf("%s : Verb\n", yytext); }
[Cc]uriosity           { printf("%s : Noun\n", yytext); }
has                   { printf("%s : Verb\n", yytext); }
its                   { printf("%s : Pronoun (Possessive)\n", yytext); }
own                   { printf("%s : Adjective\n", yytext); }
reason                { printf("%s : Noun\n", yytext); }
for                   { printf("%s : Preposition\n", yytext); }
existing              { printf("%s : Verb/Adjective\n", yytext); }
[.,;:!?]              { printf("%s : Punctuation\n", yytext); }
[ \t\n]+              { /* Ignore whitespace */ }
.                     { printf("%s : Unknown\n", yytext); }
%%

int main(void) {
    yylex();
    return 0;
}
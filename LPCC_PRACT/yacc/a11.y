%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

/* Define a union that holds a C-string */
%union {
    char *id;
}

/* Declare the IDENTIFIER token with a string semantic value */
%token <id> IDENTIFIER

/* Specify that the nonterminal 'var' carries a string value */
%type <id> var

%%
input:
      /* empty */
    | input line
    ;

line:
      var '\n' { 
          printf("Valid variable name: %s\n", $1);
          free($1);  /* free the copy allocated in the lexer */
      }
    ;

var:
      IDENTIFIER { $$ = $1; }
    ;
%%

int main(void)
{
    printf("Enter variable names (one per line):\n");
    yyparse();
    return 0;
}

void yyerror(const char *s)
{
    fprintf(stderr, "Error: %s\n", s);
}
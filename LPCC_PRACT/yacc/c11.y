%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
%}

/* Define a union that can hold a double value or a string */
%union {
    double dval;
    char*  sval;
}

/* Declare tokens with the appropriate types */
%token <sval> IDENTIFIER
%token <dval> NUMBER
%token <sval> STRING
%token SQRT STRLEN

/* We expect the built-in function subexpressions to evaluate to a double */
%type <dval> sqrt_expr strlen_expr

%%
/* A statement is an assignment where the right‐side is a built‐in function call */
stmt:
      IDENTIFIER '=' sqrt_expr {
          printf("%s = %f\n", $1, $3);
          free($1);
      }
    | IDENTIFIER '=' strlen_expr {
          printf("%s = %f\n", $1, $3);
          free($1);
      }
    ;

sqrt_expr:
      SQRT '(' NUMBER ')' { $$ = sqrt($3); }
    ;

strlen_expr:
      STRLEN '(' STRING ')' { $$ = (double) strlen($3); free($3); }
    ;
%%
  
int main(void)
{
    printf("Enter a built-in function expression:\n");
    yyparse();
    return 0;
}
  
void yyerror(const char *s)
{
    fprintf(stderr, "Error: %s\n", s);
}
%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
%}

/* The union can hold a double value or a string for an identifier */
%union {
    double dval;
    char *sval;
}

/* NUMBER returns a double, IDENTIFIER returns a string */
%token <dval> NUMBER
%token <sval> IDENTIFIER

/* Tokens for built-in functions */
%token SIN COS

/* The nonterminal expr carries a double value */
%type <dval> expr

/* Operator precedence */
%left '+' '-'
%left '*' '/'
%right UMINUS

%%
input:
      stmt '\n' { /* Do nothing */ }
    ;

stmt:
      IDENTIFIER '=' expr {
        printf("%s = %f\n", $1, $3);
        free($1);
      }
    ;

expr:
      expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { $$ = $1 / $3; }
    | '-' expr %prec UMINUS { $$ = -$2; }
    | '(' expr ')' { $$ = $2; }
    | NUMBER { $$ = $1; }
    | SIN '(' expr ')' { $$ = sin($3); }
    | COS '(' expr ')' { $$ = cos($3); }
    ;
%%

int main(void) {
    printf("Enter an expression:\n");
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
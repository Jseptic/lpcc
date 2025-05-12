%{
#include <stdio.h>
#include <stdlib.h>
%}

/* Define a union to hold a double value */
%union {
    double dval;
}

/* Declare NUMBER token and specify that its semantic value is of type double */
%token <dval> NUMBER

/* Nonterminals that hold a double value */
%type <dval> expr

/* Define operator precedence and associativity */
%left '+' '-'
%left '*' '/'
%right UMINUS

%%

/* Grammar rules */
input:
    expr { printf("Result = %f\n", $1); }
    ;

expr:
      expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { $$ = $1 / $3; }
    | '-' expr %prec UMINUS { $$ = -$2; }
    | '(' expr ')' { $$ = $2; }
    | NUMBER { $$ = $1; }
    ;

%%

int main(void)
{
    printf("Enter an arithmetic expression:\n");
    yyparse();
    return 0;
}

void yyerror(const char *s)
{
    fprintf(stderr, "Error: %s\n", s);
}
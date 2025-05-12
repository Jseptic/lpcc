%{
#include <stdio.h>
#include <stdlib.h>
%}

%union {
    double dval;
}

%token <dval> NUMBER
%type <dval> expr

%left '+' '-'
%left '*' '/'
%right UMINUS

%%
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
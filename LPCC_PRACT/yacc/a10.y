%{
#include <stdio.h>
#include <stdlib.h>
%}

%union {
    double dval;
}

%token <dval> NUMBER
%type <dval> input line expr

%left '+' '-'
%left '*' '/'
%right UMINUS

%%
input:
      /* empty input */ { $$ = 0; }
    | input line { $$ = $2; }
    ;

line:
      '\n' { $$ = 0; }
    | expr '\n' { printf("Result = %f\n", $1); $$ = $1; }
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
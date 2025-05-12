%{
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

/* Function to toggle the case of each character in a string */
char* convert(const char *s) {
    char *result = strdup(s);
    for (int i = 0; result[i] != '\0'; i++){
        if (islower(result[i]))
            result[i] = toupper(result[i]);
        else if (isupper(result[i]))
            result[i] = tolower(result[i]);
    }
    return result;
}
%}

%union {
    char *str;
}

%token <str> IDENTIFIER
%type <str> input line

%%
input:
      /* empty */
    | input line
    ;

line:
    IDENTIFIER '-' IDENTIFIER {
        char *converted = convert($1);
        printf("Input: %s, Converted: %s, Expected: %s\n", $1, converted, $3);
        free($1);
        free($3);
        free(converted);
    }
    ;
%%

int main(void)
{
    printf("Enter variable conversion lines (e.g., Pune - pUNE):\n");
    yyparse();
    return 0;
}

void yyerror(const char *s)
{
    fprintf(stderr, "Error: %s\n", s);
}
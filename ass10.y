%{
#include <stdio.h>
#include <stdlib.h>
%}
 
%token NUMBER
%left '+' '-'
%left '*' '/'
%start input
 
%union {
    double dval;
}
 
%type <dval> expr
%token <dval> NUMBER
 
%%
 
input:
    /* empty */
    | input line
    ;
 
line:
    '\n'
    | expr '\n'    { printf("= %lf\n", $1); }
    ;
 
expr:
    NUMBER         { $$ = $1; }
    | expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr {
        if ($3 == 0) {
            printf("Error: Division by zero\n");
            exit(1);
        }
        $$ = $1 / $3;
    }
    | '(' expr ')'  { $$ = $2; }
    ;
 
%%
 
int main() {
    printf("Enter expressions (Ctrl+C to quit):\n");
    yyparse();
    return 0;
}
 
int yyerror(const char *s) {
    fprintf(stderr, "Parse error: %s\n", s);
    return 0;
}

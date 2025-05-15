%{
#include <stdio.h>
%}
 
KEYWORD     auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while
IDENTIFIER  [a-zA-Z_][a-zA-Z0-9_]*
NUMBER      [0-9]+(\.[0-9]+)?
OPERATOR    \+|\-|\*|\/|%|==|!=|<=|>=|<|>|\=\=|\=|\&\&|\|\||\+\+|\-\-
DELIMITER   [;,\[\]\(\)\{\}]
 
%%
{KEYWORD}      { printf("Keyword\t\t=> %s\n", yytext); }
{IDENTIFIER}   { printf("Identifier\t=> %s\n", yytext); }
{NUMBER}       { printf("Number\t\t=> %s\n", yytext); }
{OPERATOR}     { printf("Operator\t=> %s\n", yytext); }
{DELIMITER}    { printf("Delimiter\t=> %s\n", yytext); }
\".*?\"         { printf("String Literal\t=> %s\n", yytext); }
\/\/.*         { printf("Comment\t\t=> %s\n", yytext); }
[ \t\n]+        { /* Ignore whitespace */ }
.               { printf("Unknown\t\t=> %s\n", yytext); }
%%
 
int yywrap() {
    return 1;
}
 
int main() {
    printf("Enter C code (Ctrl+D to end):\n\n");
    yylex();
    return 0;
}

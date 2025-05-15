%{
#include "expr.tab.h"
#include <stdlib.h>
%}
 
%%
 
[0-9]+\.[0-9]+    { yylval.dval = atof(yytext); return NUMBER; }
[0-9]+            { yylval.dval = atof(yytext); return NUMBER; }
[ \t]             ;  // ignore whitespace
\n                return '\n';
.                 return yytext[0];
 
%%
 
int yywrap() {
    return 1;
}

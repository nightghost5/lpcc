%{
#include <stdio.h>
%}
 
%%
"the"|"a"|"an"                              { printf("Article\t\t=> %s\n", yytext); }
"he"|"she"|"it"|"they"|"we"|"i"|"you"       { printf("Pronoun\t\t=> %s\n", yytext); }
"is"|"am"|"are"|"was"|"were"|"be"|"being"|"been" { printf("Verb\t\t\t=> %s\n", yytext); }
"have"|"has"|"had"|"do"|"does"|"did"        { printf("Verb\t\t\t=> %s\n", yytext); }
"can"|"could"|"shall"|"should"|"will"|"would"|"may"|"might"|"must" { printf("Modal Verb\t\t=> %s\n", yytext); }
"in"|"on"|"at"|"by"|"for"|"with"|"about"|"against"|"between"|"into"|"through"|"during"|"before"|"after"|"above"|"below" { printf("Preposition\t\t=> %s\n", yytext); }
"and"|"but"|"or"|"yet"|"so"|"because"       { printf("Conjunction\t\t=> %s\n", yytext); }
"very"|"too"|"quite"|"rather"|"just"|"almost"|"enough" { printf("Adverb\t\t=> %s\n", yytext); }
"not"|"never"|"always"|"often"|"sometimes" { printf("Adverb\t\t=> %s\n", yytext); }
[0-9]+                                      { printf("Number\t\t=> %s\n", yytext); }
[.!?,;:'\"-]                                 { printf("Punctuation\t=> %s\n", yytext); }
[A-Za-z]+                                   { printf("Noun/Other\t\t=> %s\n", yytext); }
[ \t\n]+                                    { /* Skip whitespace */ }
.                                           { printf("Unknown\t\t=> %s\n", yytext); }
%%
 
int yywrap() {
    return 1;
}
 
int main() {
    printf("Enter input (Ctrl+D to end):\n\n");
    yylex();
    return 0;
}

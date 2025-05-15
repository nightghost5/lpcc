%{
#include <stdio.h>
#include <string.h>
#include <ctype.h>

/*— helper to test membership in a C array of strings —*/
static int in_list(const char *w, const char *list[], int n) {
    for (int i = 0; i < n; i++)
        if (strcmp(w, list[i]) == 0) return 1;
    return 0;
}

/*— our POS word lists (all lowercase) —*/
static const char *articles[]   = { "a", "an", "the" };
static const char *preps[]      = { "to", "from", "in", "on", "of", "for", "with", "toward" };
static const char *conjuncts[]  = { "and", "but", "or", "if", "that" };
static const char *pronouns[]   = { "i", "you", "it" };
static const char *verbs[]      = { "dread", "run", "arrives", "arrive",
                                    "stop", "has", "kill", "give",
                                    "imagines", "come", "comes", "have",
                                    "divide" };
static const char *nouns[]      = { "destiny", "thing", "curiosity", "reason",
                                    "generation", "instinct", "gap" };
static const char *adjectives[] = { "strong", "basic", "dramatic", "distinct",
                                    "empty", "intelligent", "wiser", "fine",
                                    "all", "same", "generation" };
%}

/*— rules —*/
%%
[\r\n]+         { /* print a blank line to reflect input line breaks */  
                    printf("\n"); 
                }

[ \t]+          ;  /* skip spaces/tabs */

[\200-\377]+   ;  /* skip UTF-8 multibyte so smart quotes vanish */

[']             { printf("<PUNCT,        \"%s\">\n", yytext); }

[.,!?;:]        { printf("<PUNCT,        \"%s\">\n", yytext); }

[A-Za-z]+       {
                    /* lowercase into lw[], then lookup in lists */
                    char lw[128];
                    int L = yyleng < 127 ? yyleng : 127;
                    for (int i = 0; i < L; i++) lw[i] = tolower(yytext[i]);
                    lw[L] = '\0';

                    if      (in_list(lw, articles,   sizeof(articles)/sizeof(*articles)))
                        printf("<ARTICLE,      \"%s\">\n", yytext);
                    else if (in_list(lw, preps,      sizeof(preps)/sizeof(*preps)))
                        printf("<PREPOSITION,  \"%s\">\n", yytext);
                    else if (in_list(lw, conjuncts,  sizeof(conjuncts)/sizeof(*conjuncts)))
                        printf("<CONJUNCTION,  \"%s\">\n", yytext);
                    else if (in_list(lw, pronouns,   sizeof(pronouns)/sizeof(*pronouns)))
                        printf("<PRONOUN,      \"%s\">\n", yytext);
                    else if (in_list(lw, verbs,      sizeof(verbs)/sizeof(*verbs)))
                        printf("<VERB,         \"%s\">\n", yytext);
                    else if (in_list(lw, nouns,      sizeof(nouns)/sizeof(*nouns)))
                        printf("<NOUN,         \"%s\">\n", yytext);
                    else if (in_list(lw, adjectives, sizeof(adjectives)/sizeof(*adjectives)))
                        printf("<ADJECTIVE,    \"%s\">\n", yytext);
                    else
                        printf("<UNKNOWN,      \"%s\">\n", yytext);
                }

.               { /* any other single character */ 
                    printf("<UNKNOWN,      \"%s\">\n", yytext);
                }
%%

int main(void) {
    yylex();
    return 0;
}


Commands
lex file_name.l
cc lex.yy.c -o file_name -ll
./file_name < input.txt

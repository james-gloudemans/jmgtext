#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <test.h>
#include <rope.h>
#include <util.h>
#include <string.h>

char *random_string(int n)
{// Return a random string of letters of length n
    char *result = UTIL_malloc(n*sizeof(char));
    srand(time(0));
    char *alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int len = strlen(alphabet);
    for(int i=0; i<n; ++i)
    {
        result[i] = alphabet[rand() % (len)];
        printf("%c", result[i]);
    }
    printf("\n");
    return result;
}

int main(int argc, char *argv[])
{
    // char *text = "Sami is hot";
    // Rope_p rope = NULL;
    // for(int i=0; i<strlen(text); ++i)
    // {
    //     char c[2] = {text[i], '\0'};
    //     Rope_p rc = new_rope(c);
    //     rope = rope_concat(rope, rc);
    // }
    // rope = rope_balance(rope);
    // printf("Built rope: %s\n", tostring(rope));

    Rope_p rope = new_rope(random_string(103));
    printf("Built rope: %s\n", tostring(rope));

    return 0;
}


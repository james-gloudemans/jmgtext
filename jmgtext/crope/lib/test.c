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
    char *alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    int len = strlen(alphabet);
    for(int i=0; i<n; ++i)
        result[i] = alphabet[rand() % (len)];
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

    char *string;
    Rope_p rope;
    for(int p=3; p<7; ++p)
    {
        int N = pow(10, p);
        printf("For N = %d\n", N);
        string = random_string(N);
        rope = new_rope(string);
    }
    free_rope(rope);
    UTIL_FREE(string);

    return 0;
}


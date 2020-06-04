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
    clock_t t0, dt;
    for(int p=6; p<10; ++p)
    {
        int N = pow(10, p);
        printf("For N = 10^%d\n", p);

        t0 = clock();
        string = random_string(N);
        dt = 1000 * (clock() - t0) / CLOCKS_PER_SEC;
        printf("Build string: %ld s %ld ms\n", dt/1000, dt%1000);

        t0 = clock();
        rope = new_rope(string);
        dt = 1000 * (clock() - t0) / CLOCKS_PER_SEC;

        char c;
        int len = strlen(string);
        t0 = clock();
        for(int i=0; i<1000; ++i)
            c = string[rand() % len];
        dt = 1000000 * (clock() - t0) / CLOCKS_PER_SEC;
        printf("getchar string: '%c', %ld ms %ld us\n", c, dt/1000, dt%1000);

        t0 = clock();
        for(int i=0; i<1000; ++i)
            c = rope_getchar(rope, rand() % len);
        dt = 1000000 * (clock() - t0) / CLOCKS_PER_SEC;
        printf("getchar Rope: '%c', %ld ms %ld us\n", c, dt/1000, dt%1000);

        t0 = clock();
        for(int i=0; i<1000; ++i)
        {
            rope = rope_put(rope, N/2, random_string(20));
            rope = rope_remove(rope, N/2, N/2+20);
        }
        dt = 1000000 * (clock() - t0) / CLOCKS_PER_SEC;
        printf("Insert / delete Rope: '%c', %ld ms %ld us\n", c, dt/1000, dt%1000);                

        free_rope(rope);
        UTIL_FREE(string);
    }
    return 0;
}


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <test.h>
#include <rope.h>
#include <util.h>
#include <string.h>

char *random_string(int n)
{ // Return a random string of letters of length n
    char *result = UTIL_malloc(n * sizeof(char) + 1);
    srand(time(0));
    char *alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    int len = strlen(alphabet);
    for (int i = 0; i < n; ++i)
        result[i] = alphabet[rand() % (len)];
    result[n] = '\0';
    return result;
}

int main(int argc, char *argv[])
{
    char *text = "Hello, my name is Jimbo!";
    Rope_p rope = NULL;
    for (int i = 0; i < strlen(text); ++i)
    {
        char c[2] = {text[i], '\0'};
        Rope_p rc = new_rope(c);
        rope = rope_concat(rope, rc);
    }
    rope = rope_balance(rope);
    Rope_p put;
    put = rope_put(rope, 1, "123");
    printf("%s\n", tostring(put));

    // char *string;
    // Rope_p rope;
    // clock_t t0;
    // double dt;
    // for (int p = 6; p < 10; ++p)
    // {
    //     int N = pow(10, p);
    //     printf("For N = 10^%d\n", p);

    //     t0 = clock();
    //     string = random_string(N);
    //     dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    //     printf("Build string: %.2e\n", dt);

    //     t0 = clock();
    //     rope = new_rope(string);
    //     dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    //     printf("Build rope: %.2e sec\n", dt);

    //     char c;
    //     int len = strlen(string);
    //     t0 = clock();
    //     for (int i = 0; i < 1000; ++i)
    //         c = string[rand() % len];
    //     dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    //     printf("getchar string: '%c', %.2e sec\n", c, dt);

    //     t0 = clock();
    //     for (int i = 0; i < 1000; ++i)
    //         c = rope_getchar(rope, rand() % len);
    //     dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    //     printf("getchar Rope: '%c', %.2e sec\n", c, dt);

    //     int ins_len = 20;
    //     t0 = clock();
    //     for (int i = 0; i < 1000; ++i)
    //     {

    //         string = (char *)UTIL_realloc(string, (N + ins_len + 1) * sizeof(char));
    //         strcpy(string + N / 2 + ins_len, string + N / 2);
    //         strcpy(string + N / 2, random_string(20));
    //         strcpy(string + N / 2, string + N / 2 + ins_len);
    //         string = (char *)UTIL_realloc(string, (N + 1) * sizeof(char));
    //     }
    //     dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    //     printf("Insert / delete string: %.2e sec \n", dt);

    //     t0 = clock();
    //     for (int i = 0; i < 1000; ++i)
    //     {
    //         rope = rope_put(rope, N / 2, random_string(20));
    //         rope = rope_remove(rope, N / 2, N / 2 + 20);
    //     }
    //     dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    //     printf("Insert / delete Rope: %.2e sec\n", dt);

    //     free_rope(rope);
    //     UTIL_FREE(string);
    // }

    return 0;
}

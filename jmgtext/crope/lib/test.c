#include <stdio.h>
#include <test.h>
#include <rope.h>
#include <util.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char *text = "Sami is hot";
    Rope_p rope = NULL;
    for(int i=0; i<strlen(text); ++i)
    {
        char c[2] = {text[i], '\0'};
        Rope_p rc = new_rope(c);
        rope = rope_concat(rope, rc);
    }
    rope = rope_balance(rope);
    printf("Built rope: %s\n", tostring(rope));

    // printf("%d\n", rope_len(rope));
    // for(int i=0; i<rope_len(rope); ++i)
    //     printf("%c", rope_getchar(rope, i));
    // printf("\n");
    // printf("%s\n", tostring(rope));

    // Rope_tuple_p tmp = rope_cut(rope, 6);
    // Rope_p left = tmp->left;
    // Rope_p right = tmp->right;
    // printf("%s\n", tostring(left));
    // printf("%s\n", tostring(right));

    // char *str = "Hello bitches I am Yimbo.";
    // const int len = strlen(str);
    // const int i = 7;
    // char *left_text = UTIL_malloc(i+2);
    // char *right_text = UTIL_malloc(len - i);
    // left_text = strncpy(left_text, str, i);
    // right_text = strncpy(right_text, &(str[i]), len - i);
    // printf("%s\n", left_text);
    // printf("%s\n", right_text);

    return 0;
}
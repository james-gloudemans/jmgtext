#include <stdio.h>
#include <test.h>
#include <rope.h>
#include <util.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char *text = "Sami is hot";
    Rope_p rope = new_rope(NULL);
    for(int i=0; i<strlen(text); ++i)
    {
        char c[2] = {text[i], '\0'};
        Rope_p rc = new_rope(c);
        rope = rope_concat(rope, rc);
    }
    printf("%d\n", rope_len(rope));
    for(int i=0; i<rope_len(rope); ++i)
        printf("%c", rope_getchar(rope, i));
    printf("\n");

    return 0;
}
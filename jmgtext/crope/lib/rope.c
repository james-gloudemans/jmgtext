#include <stdlib.h>
#include "util.h"
#include "rope.h"

Rope_p new_rope()
{// Create a new empty rope.
    Rope_p new_rope = UTIL_NEW(Rope);
    new_rope->left = NULL;
    new_rope->right = NULL;
    new_rope->text = NULL;
    new_rope->weight = 0;
    new_rope->len = 0;
    return new_rope;
}

void free_rope(Rope_p rope)
{// Destroy the rope.
    if(rope->left != NULL)
        free_rope(rope->left);
    if(rope->right != NULL)
        free_rope(rope->right);
    free_rope_node(rope);
}

void free_rope_node(Rope_p rope)
{// Destroy the rope node.
    UTIL_FREE(rope->left);
    UTIL_FREE(rope->right);
    UTIL_FREE(rope->text);
    UTIL_FREE(rope);
}

char *tostring(Rope_p rope)
{// Convert the rope to char *.
    if(rope->text != NULL)
        return rope->text;
    char *result = "";
    if(rope->left != NULL)
        result = strcat(result, tostring(rope->left));
    if(rope->right != NULL)
        result = strcat(result, tostring(rope->right));
    return result;
}

int rope_len(Rope_p rope)
{// Return the length of the rope.
    return rope->len;
}

UTIL_BOOL_t is_rope_empty(Rope_p rope)
{// Is the rope empty?
    return rope->len == 0;
}

char rope_getchar(Rope_p rope, int i)
{// Return the character at position i.
    UTIL_ASSERT(i < rope_len(rope) && i >= 0);
    if(i >= rope->weight && rope->right != NULL)
        return rope_getchar(rope->right, i - rope->weight);
    if(rope->left != NULL)
        return rope_getchar(rope->left, i);
    return rope->text[i];
}
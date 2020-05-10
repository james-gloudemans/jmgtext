#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "util.h"
#include "rope.h"

Rope_p new_rope(char *text)
{// Create a new Rope to represent text
    Rope_p new_rope = UTIL_NEW(Rope);
    new_rope->left = NULL;
    new_rope->right = NULL;
    new_rope->text = UTIL_NEW_STR_IF(text);
    new_rope->weight = 0;
    if(text != NULL)
        new_rope->len = strlen(text);
    else
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
    char *result = UTIL_malloc(rope->len * sizeof(char));
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

Rope_p rope_concat(Rope_p first, Rope_p second)
{// Return the concatenation of two ropes.
    Rope_p parent = new_rope(NULL);
    parent->left = first;
    parent->right = second;
    parent->weight = first->len;
    parent->len = first->len + second->len;
    return parent;
}


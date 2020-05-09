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
    // How to traverse?
    return;
}

void free_rope_node(Rope_p rope)
{// Destroy the rope node
    UTIL_FREE(rope->left);
    UTIL_FREE(rope->right);
    UTIL_FREE(rope->text);
    UTIL_FREE(rope);
}
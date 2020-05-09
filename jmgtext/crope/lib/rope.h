#ifndef ROPE_H
#define ROPE_H

#include <util.h>

typedef struct {
    struct Rope *left;
    struct Rope *right;
    char *text;
    int weight;
    int len;
} Rope, *Rope_p;

typedef struct {
    Rope_p left;
    Rope_p right;
} Rope_tuple, *Rope_tuple_p;

// Create a new empty Rope
Rope_p new_rope();

// Destroy the Rope
void free_rope(Rope_p rope);

// Destroy the rope node
void free_rope_node(Rope_p rope);

// Convert the Rope to char *.
char *tostring(Rope_p rope);

// Return the length of the rope.
int rope_len(Rope_p rope);

// Is the rope empty
UTIL_BOOL_t is_rope_empty(Rope_p rope);

// Get the character at position i in the rope
char getchar(Rope_p rope, int i);

// Does the rope contain character c?
UTIL_BOOL_t rope_contains(Rope_p rope, char c);

// Return the concatenation of two ropes
Rope_p rope_concat(Rope_p first, Rope_p second);

// Return the rope duplicated n times
Rope_p rope_dupe(Rope_p rope, int n);

// Return the rope with str inserted at position i
Rope_p rope_put(Rope_p rope, int i, char *str);

// Return the rope with index i->j removed
Rope_p rope_remove(Rope_p rope, int i, int j);

// Cut the rope at position i and return the left and right ropes
Rope_tuple_p rope_cut(Rope_p rope, int i);

// Rebalance the rope
Rope_p rope_balance(Rope_p rope);

// Return the substring from position i to j
Rope_p rope_substr(Rope_p rope, int i, int j);

#endif
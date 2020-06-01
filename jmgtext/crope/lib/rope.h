#ifndef ROPE_H
#define ROPE_H

#include "util.h"

#define DEFAULT_LEAF_LEN 10

typedef struct Rope {
    struct Rope *left;
    struct Rope *right;
    char *text;
    int weight;
    int len;
} Rope, *Rope_p;

// Container for two ropes, needed for rope_cut()
typedef struct Rope_tuple {
    Rope_p left;
    Rope_p right;
} Rope_tuple, *Rope_tuple_p;

// A stack of ropes, needed for routines to iterate over nodes
typedef struct Rope_stack {
    Rope_p node;
    struct Rope_stack *next;
} Rope_stack_t, *Rope_stack_p;

// Stack functions
void push(Rope_stack_p *stack, Rope_p node);
Rope_p pop(Rope_stack_p *stack);
UTIL_BOOL isEmpty(Rope_stack_p stack);

// Create a new Rope to represent text
Rope_p new_rope(char *text);

// Create a copy of a rope node
Rope_p copy_rope_node(Rope_p node);

// Destroy the Rope
void free_rope(Rope_p rope);

// Destroy the rope node
void free_rope_node(Rope_p rope);

// Convert the Rope to char *.
char *tostring(Rope_p rope);

// Return the length of the rope.
int rope_len(Rope_p rope);

// Is the rope empty?
UTIL_BOOL is_rope_empty(Rope_p rope);

// Get the character at position i in the rope
char rope_getchar(Rope_p rope, int i);

// Does the rope contain character c?
UTIL_BOOL rope_contains(Rope_p rope, char c);

// Return the concatenation of two ropes
Rope_p rope_concat(Rope_p first, Rope_p second);

// Return the rope duplicated n times
Rope_p rope_dupe(Rope_p rope, const int n);

// Return the rope with str inserted at position i
Rope_p rope_put(Rope_p rope, const int i, char *str);

// Return the rope with index i->j removed
Rope_p rope_remove(Rope_p rope, const int i, const int j);

// Cut the rope at position i and return the left and right ropes
Rope_tuple_p rope_cut(Rope_p rope, const int i);

// Return a balanced copy of the rope
Rope_p rope_balance(Rope_p rope);

// Return the nth Fibonacci number
int _fib(const int n);

// Return the index of the largest Fibonacci number <= n
int _fib_n_gt(const int n);

// Return the substring from position i to j
Rope_p rope_substr(Rope_p rope, const int i, const int j);

// Coroutine generating the leaf nodes of the rope.
Rope_p get_leaves(Rope_p rope);

#endif
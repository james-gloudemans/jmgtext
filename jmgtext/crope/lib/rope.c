#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
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

Rope_p copy_rope_node(Rope_p node)
{// Create a copy of a rope node
    Rope_p new_node = UTIL_NEW(Rope);
    new_node->left = node->left;
    new_node->right = node->right;
    new_node->text = UTIL_NEW_STR_IF(node->text);
    new_node->weight = node->weight;
    new_node->len = node->len;
    return new_node;
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

UTIL_BOOL is_rope_empty(Rope_p rope)
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
    if(first == NULL)
        return second;
    if(second == NULL)
        return first;
    Rope_p parent = new_rope(NULL);
    parent->left = first;
    parent->right = second;
    parent->weight = first->len;
    parent->len = first->len + second->len;
    return parent;
}

Rope_tuple_p rope_cut(Rope_p rope, const int i)
{// Cut the rope at position i and return the left and right ropes
    Rope_p left_cut = copy_rope_node(rope);
    Rope_p right_cut = new_rope(NULL);
    if(i == 0)
        return & (Rope_tuple) {new_rope(NULL), rope};
    if(i == rope->len)
        return & (Rope_tuple) {rope, new_rope(NULL)};

    if(i >= rope->weight && rope->right != NULL)
    {
        if(i == rope->weight)
        {
            right_cut = rope->right;
            left_cut->right = NULL;
            left_cut->len = left_cut->left->len;
            return & (Rope_tuple) {left_cut, right_cut};
        }
        Rope_tuple_p tmp = rope_cut(rope->right, i - rope->weight);
        left_cut->right = tmp->left;
        right_cut = tmp->right;
        left_cut->weight = left_cut->left->len;
        left_cut->len = left_cut->left->len + left_cut->right->len;
        return & (Rope_tuple) {left_cut, right_cut};
    }

    if(rope->left != NULL)
    {
        Rope_tuple_p tmp = rope_cut(rope->left, i);
        left_cut->left = tmp->left;
        right_cut = tmp->right;
        left_cut->right = NULL;
        left_cut->weight = left_cut->left->len;
        left_cut->len = left_cut->left->len;
        if(rope->right != NULL)
            right_cut = rope_concat(right_cut, rope->right);
        return & (Rope_tuple) {left_cut, right_cut};
    }
    
    char *left_text = UTIL_malloc(i+2);
    char *right_text = UTIL_malloc(rope->len - i);
    left_text = strncpy(left_text, rope->text, i);
    right_text = strncpy(right_text, &(rope->text[i+1]), rope->len - i);
    left_cut = new_rope(left_text);
    right_cut = new_rope(right_text);
    return & (Rope_tuple) {left_cut, right_cut};
}

int _fib(const int n)
{// Return the nth Fibonacci number
    return (pow(1 + sqrt(5), n) - pow(1 - sqrt(5), n)) / (pow(2, n) * sqrt(5));
}

int _fib_n_gt(const int n)
{// Return the index of the smallest Fibonacci number >= n
    if(n == 1)
        return 2;
    int fib = 0;
    int i = 0;
    while(fib < n)
    {
        fib = _fib(++i);
    }
    return i;
}

Rope_p get_leaves(Rope_p rope)
{// Coroutine generating the leaf nodes of the rope.
    static Rope_p node;
    static Rope_stack_p stack;
    static int state = 0;    
    switch(state)
    {
        case 0:
            state = 1;
            node = rope;
            stack = NULL;
            while(node != NULL || !isEmpty(stack))
            {
                if(node != NULL)
                {
                    push(&stack, node);
                    node = node->left;
                }
                else
                {
                    if(!isEmpty(stack))
                    {
                        node = pop(&stack);
                        if(node->left == NULL && node->right == NULL)
                        { // Found leaf
                            return node;
                            case 1:;
                        }
                        node = node->right;
                    }
                }   
            }
    }
    state = 0;
    return NULL;
}

Rope_p rope_balance(Rope_p rope)
{// Return a balanced version of rope, see 'Ropes: an alternative to strings' for details.
    Rope_p result = NULL;
    Rope_p node;
    int numslots = _fib_n_gt(rope->len);
    Rope_p *slots = UTIL_malloc(numslots*sizeof(Rope_p));
    for(int i=0; i<numslots; ++i)
        slots[i] = NULL;
    int slot;
    for(; (node = get_leaves(rope)); )
    {
        int done = 0;
        Rope_p bal_node = copy_rope_node(node);
        while(!done)
        {
            slot = _fib_n_gt(bal_node->len) - 2;
            Rope_p prev = NULL;
            for(int i=0; i<=slot; ++i)
            {
                if(slots[i] != NULL)
                {
                    prev = rope_concat(prev, slots[i]);
                    slots[i] = NULL;
                }
            }
            if(prev != NULL)
            {
                bal_node = rope_concat(prev, bal_node);
            }
            else
            {
                slots[slot] = bal_node;
                done = 1;
            }
        }
    }
    for(int i=0; i<numslots; ++i)
        if(slots[i] != NULL)
            result = rope_concat(slots[i], result);
    return result;
}

void push(Rope_stack_p *stack, Rope_p node)
{// Push rope `node` onto the stack.
    Rope_stack_p new_node = UTIL_NEW(Rope_stack_t);
    new_node->node = node;
    new_node->next = *stack;
    (*stack) = new_node;
}

Rope_p pop(Rope_stack_p *stack)
{// Remove and return the rope from the top of the stack
    if(isEmpty(*stack))
    {
        printf("Rope stack underflow.\n");
        exit(0);
    }
    else
    {    
        Rope_stack_p top = *stack;
        Rope_p node = top->node;
        (*stack) = top->next;
        UTIL_FREE(top);
        return node;
    }
}

UTIL_BOOL isEmpty(Rope_stack_p stack)
{// Is the stack empty
    return stack == NULL;
}

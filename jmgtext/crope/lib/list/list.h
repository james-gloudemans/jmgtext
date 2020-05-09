#ifndef LIST_H
#define LIST_H

// Node in a doubly-linked list
typedef struct list_node
{
    struct list_node *next;
    struct list_node *prev;
    void *data;

} LIST_NODE_t, *LIST_NODE_p_t;

// Construct and return a new list node.
LIST_NODE_p_t create_list_node(void *data, size_t size);

// Destroy a list node.
void free_list_node(LIST_NODE_p_t node);

// An anchor for a circular doubly-linked list
typedef LIST_NODE_t LIST_ANCHOR_t, *LIST_ANCHOR_p_t;

// Create and return a new list
LIST_ANCHOR_p_t create_list(void);

// Destroy a list
void free_list(LIST_ANCHOR_p_t list);

// Is the node enqueued in a list?
UTIL_BOOL_t is_node_enqd(LIST_NODE_p_t node);

// Is the list empty?
UTIL_BOOL_t is_list_empty(LIST_ANCHOR_p_t list);

// Push node to head of the list
void push_head(LIST_ANCHOR_p_t list, LIST_NODE_p_t node);

// Push node to tail of the list
void push_tail(LIST_ANCHOR_p_t list, LIST_NODE_p_t node);

// Remove and return the head
LIST_NODE_p_t pop_head(LIST_ANCHOR_p_t list);

// Remove and return the tail
LIST_NODE_p_t pop_tail(LIST_ANCHOR_p_t list);

// Return the head
LIST_NODE_p_t peek_head(LIST_ANCHOR_p_t list);

//Return the tail
LIST_NODE_p_t peek_tail(LIST_ANCHOR_p_t list);

// Remove and return the node from the list
LIST_NODE_p_t dequeue_item(LIST_NODE_p_t node);

// Return the node at position i in the list
LIST_NODE_p_t get(LIST_ANCHOR_p_t list, int i);

// Return the node at position i traversing the list in reverse
LIST_NODE_p_t get_reversed(LIST_ANCHOR_p_t, int i);

// Insert node in to list at position i
void insert(LIST_ANCHOR_p_t list, LIST_NODE_p_t node, const unsigned int i);

// Return the next node in the list
LIST_NODE_p_t get_next(LIST_NODE_p_t node);

// Return the previous node in the list
LIST_NODE_p_t get_prev(LIST_NODE_p_t node);

// Return the data on the node
void *get_data(LIST_NODE_p_t node);

// Return the length of the list
int get_len(LIST_ANCHOR_p_t list);

#endif
#include <stdlib.h>
#include <util.h>
#include <list.h>

LIST_NODE_p_t create_list_node(void *data, size_t size)
{/* Construct and return a new list node */
    UTIL_ASSERT(data != NULL);
    LIST_NODE_p_t new_list_node = UTIL_NEW(LIST_NODE_p_t);
    new_list_node->next = new_list_node;
    new_list_node->prev = new_list_node;

    size_t node_size = size + 2*sizeof(LIST_NODE_p_t) + sizeof(void*);
    new_list_node->data = malloc(node_size);
    if(new_list_node->data == NULL)
        abort();
    memcpy(new_list_node->data, data, node_size);

    return new_list_node;
}

void free_list_node(LIST_NODE_p_t node)
{/* Destroy a list node */
    UTIL_FREE(node->data);
    UTIL_FREE(node);
}

LIST_ANCHOR_p_t create_list()
{/* Create and return a new list. */
    LIST_ANCHOR_p_t list = UTIL_NEW(LIST_ANCHOR_t);
    list->next = list;
    list->prev = list;
    return list;
}

void free_list(LIST_ANCHOR_p_t list)
{/* Destroy a list */
    if(is_list_empty(list))
        return;
    LIST_NODE_p_t node = list;
    LIST_NODE_p_t next = list->next;
    while(node != NULL)
    {
        next = node->next;
        UTIL_FREE(node);
        node = next;
    }
}

UTIL_BOOL_t is_node_enqd(LIST_NODE_p_t node)
{/* Test if node is enqueued to a list already. */
    return (node->next == node ? UTIL_FALSE : UTIL_TRUE);
}

UTIL_BOOL_t is_list_empty(LIST_ANCHOR_p_t list)
{/* Test if list is empty */
    return (list->next == list ? UTIL_TRUE : UTIL_FALSE);
}

void push_head(LIST_ANCHOR_p_t list, LIST_NODE_p_t node)
{/* Push node to the front of the list. */
    UTIL_ASSERT(!is_node_enqd(node));
    LIST_NODE_p_t head = list->next;
    node->next = head;
    node->prev = list;
    head->prev = node;
    list->next = node;    
}

void push_tail(LIST_ANCHOR_p_t list, LIST_NODE_p_t node)
{/* Push node to the tail of the list. */
    UTIL_ASSERT(!is_node_enqd(node));
    LIST_NODE_p_t tail = list->prev;
    node->prev = tail;
    node->next = list;
    tail->next = node;
    list->prev = node;
}

LIST_NODE_p_t pop_head(LIST_ANCHOR_p_t list)
{/* Remove and return the head of the list */
    LIST_NODE_p_t head = list->next;
    list->next = head->next;
    head->next->prev = list;
    head->next = head;
    head->prev = head;
    return head;
}

LIST_NODE_p_t pop_tail(LIST_ANCHOR_p_t list)
{/* Remove and return the tail of the list */
    LIST_NODE_p_t tail = list->prev;
    list->prev = tail->prev;
    tail->prev->next = list;
    tail->next = tail;
    tail->prev = tail;
    return tail;
}

LIST_NODE_p_t peek_head(LIST_ANCHOR_p_t list)
{/* Return the head of the list */
    return list->next;
}

LIST_NODE_p_t peek_tail(LIST_ANCHOR_p_t list)
{/* Return the tail of the list. */
    return list->prev;
}

LIST_NODE_p_t dequeue_item(LIST_NODE_p_t node)
{/* Remove and return node from the list */
    node->prev->next = node->next;
    node->next->prev = node->prev;
    node->next = node;
    node->prev = node;
    return node;
}

LIST_NODE_p_t get(LIST_ANCHOR_p_t list, int i)
{/* Return the node from position i in the list. */
    if(is_list_empty(list))
        return NULL;
    LIST_NODE_p_t node;
    int j;
    for(node = list->next, j=0; node != list; node = node->next, ++j)
        if(j == i)
            return node;
    return NULL;
}

LIST_NODE_p_t get_reversed(LIST_ANCHOR_p_t list, int i)
{/* Return the node at position i traversing the list in reverse */
    if(is_list_empty(list))
        return NULL;
    LIST_NODE_p_t node;
    int j;
    for(node = list->prev, j=0; node != list; node = node->prev, ++j)
        if(j == i)
            return node;
    return NULL;
}

void insert(LIST_ANCHOR_p_t list, LIST_NODE_p_t node, const unsigned int i)
{/* Insert node in to list at position i */
    LIST_NODE_p_t next_node = get(list, i);
    if(next_node == NULL)
        push_tail(list, node);
    else
    {
        node->next = next_node;
        node->prev = next_node->prev;
        next_node->prev->next = node;
        next_node->prev = node;
    }
}

LIST_NODE_p_t get_next(LIST_NODE_p_t node)
{/* Return the next node in the list */
    return node->next;
}

LIST_NODE_p_t get_prev(LIST_NODE_p_t node)
{/* Return the previous node in the list */
    return node->prev;
}

void *get_data(LIST_NODE_p_t node)
{/* Return the data on the node */
    return node->data;
}

int get_len(LIST_ANCHOR_p_t list)
{/* Return the length of the list */
    LIST_NODE_p_t node = list->next;
    int len = 0;
    while(node != list)
    {
        node = node->next;
        ++len;
    }
    return len;
}

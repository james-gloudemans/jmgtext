#ifndef UTIL_H
#define UTIL_H

#include <stdlib.h>
#include <assert.h>
#include <bsd/string.h>

#define UTIL_TRUE (1)
#define UTIL_FALSE (0)

#define UTIL_ASSERT(exp) (assert((exp)))
#define UTIL_CARD(arr) (sizeof((arr)) / sizeof(*(arr)))
#define UTIL_NEW(type) ((type *)UTIL_malloc(sizeof(type)))
#define UTIL_NEW_STR(str) (strcpy((char *)UTIL_malloc(strlen((str)) + 1), (str)))
#define UTIL_NEW_STR_IF(str) ((str) == NULL ? NULL : UTIL_new_str((str)))
#define UTIL_FREE(p)  do { UTIL_free(p); p = NULL; } while (0)

typedef char UTIL_BOOL;

void *UTIL_malloc(size_t size);
void *UTIL_calloc(size_t num, size_t size);
void *UTIL_realloc(void *ptr, size_t new_size);
void UTIL_free(void *mem);

char *UTIL_new_str(char *str);

#endif

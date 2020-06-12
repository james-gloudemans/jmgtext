#include <stdlib.h>
#include <util.h>
#include <bsd/string.h>

void *UTIL_malloc(size_t size)
{
    void *mem = malloc(size);
    if (mem == NULL && size > 0)
        abort();

    return mem;
}

void *UTIL_calloc(size_t num, size_t size)
{
    void *mem = calloc(num, size);
    if (mem == NULL && num > 0)
        abort();

    return mem;
}

void *UTIL_realloc(void *ptr, size_t new_size)
{
    void *mem = realloc(ptr, new_size);
    if (mem == NULL && new_size > 0)
        abort();

    return mem;
}

void UTIL_free(void *mem)
{
    UTIL_ASSERT(mem != NULL);
    free(mem);
}

char *UTIL_new_str(char *str)
{
    size_t str_len = strlen(str);
    char *result = (char *)UTIL_malloc(str_len + 1);
    strlcpy(result, str, str_len + 1);
    return result;
}
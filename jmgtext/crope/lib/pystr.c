#include <stdio.h>
#include <stdlib.h>
#include <bsd/string.h>
#include "util.h"
#include "pystr.h"

pystr new_str(char *init)
{ // Create a new PyString from char *.
    pystr result = UTIL_NEW(pystr_t);
    result->txt = UTIL_NEW_STR_IF(init);
    result->len = strlen(result->txt);
    return result;
}

pystr new_str_len(char *init, size_t len)
{ // Create a new PyString from char * with given length.
    pystr result = UTIL_NEW(pystr_t);
    result->txt = UTIL_NEW_STR_IF(init);
    if (len == -1)
        result->len = strlen(result->txt);
    else
        result->len = len;
    return result;
}

void free_str(pystr str)
{ // Destroy the PyString.
    if (str->txt != NULL)
        UTIL_FREE(str->txt);
    UTIL_FREE(str);
}

pystr copy_str(pystr str)
{ // Return a copy of PyString str.
    if (str != NULL && str->txt != NULL)
        return new_str_len(str->txt, str_len(str));
    else
        return new_str(NULL);
}

int str_len(pystr str)
{ // Return the length of the PyString.
    UTIL_ASSERT(str != NULL);
    return str->len;
}

char *
get_str(pystr str)
{ // Return a pointer to the text in the PyString.
    UTIL_ASSERT(str != NULL);
    return str->txt;
}

UTIL_BOOL
is_str_empty(pystr str)
{ // Is the PyString empty?
    return str_len(str) == 0;
}

char str_getchar(pystr str, const int i)
{ // Return the char at position i in the PyString.
    UTIL_ASSERT(str != NULL && str_len(str) > i);
    return str->txt[i];
}

pystr str_substr(pystr str, const int i, const int j)
{ // Return the substring from position i to j.
    UTIL_ASSERT(str != NULL && j > i && j < str_len(str));
    size_t new_len = j - i;
    char *new_txt = (char *)UTIL_malloc(new_len + 1);
    new_txt[0] = '\0';
    strlcat(new_txt, str->txt + i, new_len + 1);
    return new_str_len(new_txt, new_len);
}

UTIL_BOOL
str_contains(pystr str, const char c)
{ // Does the PyString contain character c?
    UTIL_ASSERT(str != NULL);
    if (str->txt == NULL)
        return UTIL_FALSE;
    for (int i = 0; i < str->len; ++i)
        if (str->txt[i] == c)
            return UTIL_TRUE;
    return UTIL_FALSE;
}

pystr str_concat(pystr left, pystr right)
{ // Return the concatenation of PyStrings left and right.
    UTIL_ASSERT(left != NULL && right != NULL);
    char *result = UTIL_NEW_STR_IF(left->txt);
    size_t new_len = str_len(left) + str_len(right);
    strlcat(result, UTIL_NEW_STR_IF(right->txt), new_len + 1);
    return new_str_len(result, new_len);
}

pystr str_dupe(pystr str, const int n)
{ // Return the PyString duplicated n times.
    size_t new_len = n * str_len(str);
    char *result_txt = (char *)UTIL_malloc(new_len + 1);
    result_txt[0] = '\0';
    for (int i = 0; i < n; ++i)
        strlcat(result_txt, str->txt, str_len(str) * (i + 1) + 1);
    return new_str_len(result_txt, new_len);
}

pystr str_put(pystr str, const int i, pystr ins_str)
{ // Return the PyString with ins_str inserted at position i.
    UTIL_ASSERT(str != NULL && i <= str_len(str) && ins_str != NULL);
    size_t new_len = str_len(str) + str_len(ins_str);
    char *result_txt = (char *)UTIL_malloc(new_len + 1);
    result_txt[0] = '\0';
    strlcat(result_txt, str->txt, i + 1);
    strlcat(result_txt, ins_str->txt, strlen(result_txt) + str_len(ins_str) + 1);
    strlcat(result_txt, str->txt + i, new_len + 1);
    return new_str_len(result_txt, new_len);
}

pystr chars_put(pystr str, const int i, char *ins_str)
{// Return the PyString with ins_str inserted at position i
    return str_put(str, i, new_str(ins_str));
}

pystr str_remove(pystr str, const int i, const int j)
{ // Return the PyString with position i->j removed.
    UTIL_ASSERT(str != NULL && i < j && j <= str_len(str));
    size_t new_len = str_len(str) - (j - i);
    char *result_txt = (char *)UTIL_malloc(new_len + 1);
    result_txt[0] = '\0';
    strlcat(result_txt, str->txt, i + 1);
    strlcat(result_txt, str->txt + j, new_len + 1);
    return new_str_len(result_txt, new_len);
}

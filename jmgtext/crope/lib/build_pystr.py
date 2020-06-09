#!/usr/bin/python3
from cffi import FFI

builder = FFI()

builder.cdef(
    """
typedef char UTIL_BOOL;

typedef struct PyString {
    char *txt;
    int len;
} pystr_t, *pystr;

// Create a new PyString from char *.
pystr
new_str(char *init);

// Destroy the PyString.
void
free_str(pystr str);

// Return a copy of PyString str
pystr
copy_str(pystr str);

// Return the length of the PyString.
int
str_len(pystr str);

// Return a pointer to the text in the PyString.
char *
get_str(pystr str);

// Is the PyString empty?
UTIL_BOOL
is_str_empty(pystr str);

// Return the char at position i in the PyString.
char
str_getchar(pystr str, const int i);

// Return the substring from position i to j
pystr
str_substr(pystr str, const int i, const int j);

// Does the PyString contain character c?
UTIL_BOOL
str_contains(pystr str, const char c);

// Return the concatenation of PyStrings left and right.
pystr
str_concat(pystr left, pystr right);

// Return the PyString duplicated n times.
pystr
str_dupe(pystr str, const int n);

// Return the PyString with ins_str inserted at position i.
pystr
str_put(pystr str, const int i, pystr ins_str);

// Return the PyString with position i->j removed.
pystr
str_remove(pystr str, const int i, const int j);
"""
)

builder.set_source(
    "_cffi_pystr",
    """
#include "util.h"
#include "pystr.h"
""",
    libraries=["pystr"],
    library_dirs=["/home/james/projects/jmgtext/jmgtext/crope/lib"],
    extra_link_args=["-Wl,-rpath=" + "/home/james/projects/jmgtext/jmgtext/crope/lib"],
)

if __name__ == "__main__":
    builder.compile(verbose=True)

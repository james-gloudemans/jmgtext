#!/usr/bin/python3
from cffi import FFI

builder = FFI()

builder.cdef(
    """

"""
)

builder.set_source(
    "_cffi_rope",
    """
#include "util.h"
#include "rope.h"
""",
    libraries=["rope"],
    library_dirs=["/home/james/projects/crope/lib"],
    extra_link_args=["-Wl,-rpath=" + "/home/james/projects/crope/lib"],
)

if __name__ == "__main__":
    builder.compile(verbose=True)

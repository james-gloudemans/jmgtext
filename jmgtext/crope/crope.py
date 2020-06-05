"""crope.py: Python + cffi wrapper for C rope."""
# Standard Library
from collections.abc import Sequence
import weakref
from typing import Iterator, Union

# Local imports
from lib._cffi_rope import ffi, lib

# Type aliases
Stringy = Union[str, bytes, "Rope"]

global_keydict: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


class Rope(Sequence):
    """
    Rope(object='') -> Rope.

    Create a new Rope object from the given object.
    """

    def __init__(self, s: Stringy = b"", *, crope=None) -> None:
        """Initialize a new Rope."""
        if crope is not None:
            global_keydict[self] = crope
            self._crope = crope
        else:
            if isinstance(s, Rope):
                global_keydict[self] = s._crope
                self._crope = s._crope
            else:
                if isinstance(s, str):
                    s = bytes(s, encoding="utf-8")
                global_keydict[self] = lib.new_rope(s)
                self._crope = global_keydict[self]

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"Rope({str(self)})"

    def __str__(self) -> str:
        """Return str(self)."""
        # return f"{str(ffi.string(lib.tostring(self._crope)), 'utf-8')}"
        return f"{ffi.string(lib.tostring(self._crope))}"

    def __len__(self) -> int:
        """Return len(self)."""
        return lib.rope_len(self._crope)

    def __bool__(self) -> bool:
        """Return bool(self)."""
        return len(self) > 0

    def __getitem__(self, i) -> str:
        """Return self[i]."""
        return str(lib.rope_getchar(self._crope, i), "utf-8")

    def __iter__(self) -> Iterator[str]:
        """Return iter(self)."""
        node = lib.get_leaves(self._crope)
        while node != ffi.NULL:
            yield from str(ffi.string(node.text), "utf-8")
            node = lib.get_leaves(self._crope)

    def __add__(self, other: Stringy) -> "Rope":
        """Return self + other."""
        if not isinstance(other, Rope):
            other = Rope(other)
        return Rope(crope=lib.rope_concat(self._crope, other._crope))

    def __iadd__(self, other: Stringy) -> "Rope":
        """Set self to self + other."""
        return self + other

    def __mul__(self, other: int) -> "Rope":
        if not isinstance(other, int):
            raise TypeError("can't multiply sequence by non-int of type 'float'")
        return Rope(crope=lib.rope_dupe(self._crope, other))

    def put(self, i: int, s: Stringy) -> "Rope":
        """Return a copy of self with s inserted at index i."""
        if isinstance(s, Rope):
            s = bytes(str(s), "utf-8")
        if isinstance(s, str):
            s = bytes(s, "utf-8")
        return Rope(crope=lib.rope_put(self._crope, i, s))

    def delete(self, i: int, j: int) -> "Rope":
        """Return a copy of self with self[i:j] removed."""
        return Rope(crope=lib.rope_remove(self._crope, i, j))


if __name__ == "__main__":

    string = "Hello, my name is Yimbo!"
    r = Rope(string)
    s = r + r
    print("".join(c for c in s))

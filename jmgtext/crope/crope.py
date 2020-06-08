"""crope.py: Python + cffi wrapper for C rope."""
# Standard Library
from collections.abc import Sequence

# import weakref
from typing import Iterator, Union

# Local imports
from lib._cffi_rope import ffi, lib

# Type aliases
Stringy = Union[str, bytes, "Rope"]


class Rope(Sequence):
    """
    Rope(object='') -> Rope.

    Create a new Rope object from the given object.
    """

    def __init__(self, s: Stringy = b"", *, crope=None) -> None:
        """Initialize a new Rope."""
        if crope is not None:
            self._crope = lib.copy_rope_node(crope)
        else:
            if isinstance(s, Rope):
                self._crope = lib.copy_rope_node(s._crope)
            else:
                if isinstance(s, str):
                    s = bytes(s, encoding="utf-8")
                self._crope = lib.new_rope(s)

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"Rope({str(self)})"

    def __str__(self) -> str:
        """Return str(self)."""
        return f"{str(ffi.string(lib.tostring(self._crope)), 'utf-8')}"
        # return f"{ffi.string(lib.tostring(self._crope))}"

    def __len__(self) -> int:
        """Return len(self)."""
        return lib.rope_len(self._crope)

    def __bool__(self) -> bool:
        """Return bool(self)."""
        return len(self) > 0

    def __eq__(self, other) -> bool:
        """Return self == other."""
        if not (
            isinstance(other, str)
            or isinstance(other, bytes)
            or isinstance(other, Rope)
        ):
            return NotImplemented
        return str(self) == str(other)

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

    import string
    import random
    from jmgtext.timer import Timer

    def random_string(length: int) -> str:
        """Return random string of specified length."""
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    for N in [10 ** n for n in range(3, 9)]:
        print(f"N = {N:.0e}")
        with Timer(name="Build string"):
            long_string = random_string(N)
        with Timer(name="Build rope"):
            long_rope = Rope(long_string)

        with Timer(name="Get char from rope"):
            for _ in range(100):
                c = long_rope[random.choice(range(N))]

        with Timer(name="Get char from string"):
            for _ in range(100):
                c = long_string[random.choice(range(N))]

        s = random_string(100)
        with Timer(name="Insert / delete rope"):
            for _ in range(100):
                new_rope = long_rope.put(N // 2, s)
                new_rope = new_rope.delete(N // 2, N // 2 + 10)

        with Timer(name="Insert / delete string"):
            for _ in range(100):
                new_string = "".join((long_string[: N // 2], s, long_string[N // 2 :]))
                new_string = new_string[: N // 2] + new_string[N // 2 + 10 :]

        print("----------------------")

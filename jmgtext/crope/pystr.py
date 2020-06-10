"""pystr.py: Python + cffi wrapper for C string."""
# Standard Library
from collections.abc import Sequence
from typing import Iterator, Union

# Local imports
from lib._cffi_pystr import ffi, lib


class Pystr(Sequence):
    """
    Pystr(object='') -> Pystr

    Create a new Pystr object from the given object.
    """

    def __init__(self, obj="") -> None:
        """Initialize a new Pystr."""
        if isinstance(obj, str):
            self._str = lib.new_str(bytes(obj, encoding="utf-8"))
        elif isinstance(obj, bytes):
            self._str = lib.new_str(obj)
        else:
            raise NotImplementedError()

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"Pystr({str(self)})"

    def __str__(self) -> str:
        """Return str(self)."""
        return ffi.string(lib.get_str(self._str)).decode(encoding="utf-8")

    def __len__(self) -> int:
        """Return len(self)."""
        return lib.str_len(self._str)

    def __getitem__(self, i) -> Union[str, "Pystr"]:
        """Return self[i]."""
        if isinstance(i, int):
            return lib.str_getchar(self._str, i).decode(encoding="utf-8")
        if isinstance(i, slice):
            start = i.start if i.start is not None else 0
            stop = i.stop if i.stop is not None else len(self)
            result_txt = lib.str_substr(self._str, start, stop)
            result = Pystr()
            result._str = result_txt
            return result
        else:
            raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        """Return iter(self)."""
        yield from ffi.string(lib.get_str(self._str)).decode(encoding="utf-8")

    def __del__(self) -> None:
        """del self."""
        lib.free_str(self._str)

    def __contains__(self, s: object) -> bool:
        """Return s in self."""
        if not (isinstance(s, str) and len(s) == 1):
            raise ValueError("Can only test for membership in Pystr with chars.")
        result = lib.str_contains(self._str, bytes(s, encoding="utf-8"))
        return result == b"\x01"

    def __add__(self, other) -> "Pystr":
        """Return self + other."""
        if isinstance(other, str) or isinstance(other, bytes):
            other = Pystr(other)
        if not isinstance(other, Pystr):
            raise TypeError("Can only add string-like types to Pystr.")
        result = Pystr()
        result._str = lib.str_concat(self._str, other._str)
        return result

    def __iadd__(self, other) -> "Pystr":
        """Set self to self + other."""
        return self + other

    def __radd__(self, other) -> "Pystr":
        """Return other + self."""
        if isinstance(other, str) or isinstance(other, bytes):
            other = Pystr(other)
        if not isinstance(other, Pystr):
            raise TypeError("Can only add string-like types to Pystr.")
        result = Pystr()
        result._str = lib.str_concat(other._str, self._str)
        return result

    def __mul__(self, n: int) -> "Pystr":
        """Return self * n."""
        result = Pystr()
        result._str = lib.str_dupe(self._str, n)
        return result

    def __imul__(self, n: int) -> "Pystr":
        """Set self to self * n."""
        return self * n

    def __rmul__(self, n: int) -> "Pystr":
        """Return n * self."""
        return self * n

    def put(self, i: int, s) -> "Pystr":
        """Return copy of self with s inserted at position i."""
        if isinstance(s, Pystr):
            s = ffi.string(lib.get_str(s._str))
        if isinstance(s, str):
            s = bytes(s, encoding="utf-8")
        if not isinstance(s, bytes):
            raise TypeError("Can only insert string-like objects into Pystr")
        result = Pystr()
        result._str = lib.chars_put(self._str, i, s)
        return result

    def remove(self, i: int, j: int) -> "Pystr":
        """Return a copy of self with chars [i,j) removed."""
        result = Pystr()
        result._str = lib.str_remove(self._str, i, j)
        return result


if __name__ == "__main__":
    import string
    import random
    from jmgtext.timer import Timer

    def random_string(length: int) -> str:
        """Return random string of specified length."""
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    for N in (10 ** n for n in range(3, 8)):
        print(f"N = {N:.0e}")
        with Timer(name="Build string"):
            long_string = random_string(N)
        with Timer(name="Build Pystr"):
            long_pystr = Pystr(long_string)

        with Timer(name="Get char from Pystr"):
            for _ in range(100):
                c = long_pystr[random.choice(range(N))]

        with Timer(name="Get char from string"):
            for _ in range(100):
                c = long_string[random.choice(range(N))]

        s = random_string(100)
        with Timer(name="Insert / delete Pystr"):
            for _ in range(100):
                new_pystr = long_pystr.put(N // 2, s)
                new_pystr = new_pystr.remove(N // 2, N // 2 + 100)

        with Timer(name="Insert / delete string"):
            for _ in range(100):
                new_string = "".join((long_string[: N // 2], s, long_string[N // 2 :]))
                new_string = new_string[: N // 2] + new_string[N // 2 + 100 :]

        print("----------------------")

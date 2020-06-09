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
            return ffi.string(lib.str_getchar(self._str, i)).decode(encoding="utf-8")
        if isinstance(i, slice):
            result_txt = lib.str_substr(self._str, i.start, i.stop)
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


if __name__ == "__main__":
    s = Pystr("Hello my name is Yimbo!")
    print(3 * s)

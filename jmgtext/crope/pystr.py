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
            start = i.start or 0
            stop = i.stop or len(self)
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

    def put(self, s, i: int) -> "Pystr":
        """Return copy of self with s inserted at position i."""
        if isinstance(s, str) or isinstance(s, bytes):
            s = Pystr(s)
        if not isinstance(s, Pystr):
            raise TypeError("Can only insert string-like objects into Pystr")
        result = Pystr()
        result._str = lib.str_put(
            self._str, i, s._str
        )  # Does s._str get garbage collected after this?
        return result


if __name__ == "__main__":
    s = Pystr("Hello my name is Yimbo!")
    t = Pystr("123")
    print(len(s))
    print(len(t))
    print("Original: ", end="")
    for c in s:
        print(c, end="")
    print()
    print(f"3->7: {str(s[3:7])}")
    print(f"0->3: {str(s[:3])}")
    print("H in s: " + str("H" in s))
    print("A in s: " + str("A" in s))
    print(f"s x 2: {str(2*s)}")
    print(f"s + t: {str(s+t)}")
    print(f"'123' at 1: {str(s.put('123', 1))}")
    # print(f"'123' at 0: {str(s.put('123', 0))}")
    # print(f"'123' at end: {str(s.put('123', len(s)))}")

"""pystr.py: Python + cffi wrapper for C string."""
# Standard Library
from collections.abc import Sequence
from typing import Iterator

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

    def __getitem__(self, i) -> str:
        """Return self[i]."""
        if isinstance(i, int):
            return ffi.string(lib.str_getchar(self._str, i)).decode(encoding="utf-8")
        else:
            raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        """Return iter(self)."""
        yield from ffi.string(lib.get_str(self._str)).decode(encoding="utf-8")

    def __del__(self) -> None:
        """del self."""
        lib.free_str(self._str)


if __name__ == "__main__":
    s = Pystr("Hello my name is Yimbo!")
    for c in s:
        print(c, end="")
    print()

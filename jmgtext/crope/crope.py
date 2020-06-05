"""crope.py: Python + cffi wrapper for C rope."""
# Standard Library
from collections.abc import Sequence
from typing import Iterator, Union

# Local imports
from lib._cffi_rope import ffi, lib


class Rope(Sequence):
    """
    Rope(object='') -> Rope.

    Create a new Rope object from the given object.
    """

    def __init__(self, s: Union[str, bytes] = b"") -> None:
        """Initialize a new Rope."""
        if isinstance(s, str):
            s = bytes(s, encoding='utf8')
        self._crope = lib.new_rope(s)

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f'Rope({str(self)})'

    def __str__(self) -> str:
        """Return str(self)."""
        return f"{ffi.string(lib.tostring(self._crope)).decode('utf8')}"

    def __len__(self) -> int:
        """Return len(self)."""
        return lib.rope_len(self._crope)

    def __bool__(self) -> bool:
        """Return bool(self)."""
        return len(self) > 0

    def __getitem__(self, i) -> str:
        """Return self[i]."""
        return lib.rope_getchar(self._crope, i).decode('utf8')

    def __iter__(self) -> Iterator[str]:
        """Return iter(self)."""
        node = lib.get_leaves(self._crope)
        while node != ffi.NULL:
            yield from ffi.string(node.text).decode('utf8')
            node = lib.get_leaves(self._crope)


if __name__ == '__main__':

    r = Rope(b'Hello, my name is Yimbo!')
    for c in r:
        print(c)

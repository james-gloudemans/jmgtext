"""
rope.py: Immutable sequence type to efficiently operate on long strings.

TODO:
    MINIMAL:
    substring search
    ---------------------
    EXPANSIONS:
    add support for bytes
    make __getitem__ return a rope instead of str
    caching for faster __getitem__
    More of the string operations
"""
# standard library
import itertools as it
import operator as op
from collections import deque
from collections.abc import Sequence
from math import sqrt
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

# third party libraries
import more_itertools as mit

# local modules

# Type aliases
Stringy = Union[str, "Rope"]  # add bytes?


class Rope(Sequence):
    """
    Rope(object='') -> Rope.

    Create a new Rope object from the given object.
    """

    # Instance variables
    _left: Optional["Rope"]
    _right: Optional["Rope"]
    _text: str
    _weight: int
    _len: int

    # Static variables
    _default_leaf_len: int = 10000

    def __init__(self, s: Any = "", *, root: "Rope" = None) -> None:
        """Initialize self.  See type(self).__doc__ for more info."""
        if not root:
            if not isinstance(s, str):
                s = str(s)
            if len(s) <= Rope._default_leaf_len:
                # Left and right subtrees
                self._left = None
                self._right = None
                # Substring stored on the node, always == '' except for leaf nodes
                self._text = str(s)
                # Weight is the length of the left subtree, or length of the string for leaves
                self._weight = len(s)
                self._len = len(s)
            else:  # Break up long strings
                words = [
                    "".join(word)
                    for word in mit.grouper(s, Rope._default_leaf_len, fillvalue="")
                ]
                ropes: List["Rope"] = list(map(Rope, words))
                for i in range(len(words) // 2):
                    # add strings in pairs to reduce imbalance
                    ropes = list(it.starmap(op.add, mit.windowed(ropes, 2, step=2)))
                    if i % 50000 == 0:
                        ropes = [r._rebalance() for r in ropes]
                rope = list(ropes)[0]._rebalance()
                self._left, self._right = rope._left, rope._right
                self._text = rope._text
                self._weight = rope._weight
                self._len = rope._len
        else:  # copy
            self._left = root._left
            self._right = root._right
            self._text = root._text
            self._weight = root._weight
            self._len = root._len

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"Rope({str(self)})"

    def __str__(self) -> str:
        """Return str(self)."""
        return "".join(self._words())

    def __eq__(self, other) -> bool:
        """Return self == other."""
        if not (isinstance(other, Rope) or isinstance(other, str)):
            return NotImplemented
        return str(self) == str(other)

    def __len__(self) -> int:
        """Return len(self)."""
        return self._len

    def __bool__(self) -> bool:
        """Return bool(self)."""
        return self._len > 0

    def __getitem__(self, i) -> str:
        """Return self[i]."""
        if isinstance(i, slice):
            return str(self._substring(i.start or 0, i.stop))[:: i.step]
        if i < 0:
            i += len(self)
        if i < 0 or i >= len(self):
            raise IndexError
        if i >= self._weight and self._right:
            return self._right[i - self._weight]
        if self._left:
            return self._left[i]
        return self._text[i]

    def __contains__(self, sub: Stringy) -> bool:
        """Return sub in self."""
        if isinstance(sub, Rope):
            sub = str(sub)
        return sub in str(self)

    def __reversed__(self) -> Iterator[str]:
        """Return reversed(self)."""
        if self._right:
            yield from reversed(self._right)
        if self._left:
            yield from reversed(self._left)
        if self._text:  # self is a leaf node
            yield from reversed(self._text)

    def __iter__(self) -> Iterator[str]:
        """Return iter(self).  Same behavior as iter(str)."""
        if self._left:
            yield from self._left
        if self._right:
            yield from self._right
        if self._text:  # self is a leaf node
            yield from self._text

    def __add__(self, other: Stringy) -> "Rope":
        """Return self + other."""
        if isinstance(other, str):
            other = Rope(other)
        if not self:
            return other
        if not other:
            return self
        new_root = Rope()
        new_root._left = self
        new_root._right = other
        new_root._weight = len(self)
        new_root._len = len(self) + len(other)
        return new_root

    def __iadd__(self, other: Stringy) -> "Rope":
        """Return self + other."""
        return self + other

    def __mul__(self, other: int) -> "Rope":
        """Return self * other."""
        if not isinstance(other, int):
            raise TypeError("can't multiply sequence by non-int of type 'float'")
        result = Rope()
        for _ in range(other):
            result += Rope(root=self)
        return result

    def __imul__(self, other: int) -> "Rope":
        """Return self * other."""
        return self * other

    def __hash__(self) -> int:
        """Return hash(str(self))."""
        return hash(str(self))

    def index(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """Return str(self).index(sub, start, end)."""
        return str(self).index(sub, start, end)

    def count(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """Return str(self).index(sub, start, end)."""
        return str(self).count(sub, start, end)

    def put(self, i: int, s: Stringy) -> "Rope":
        """Return a copy of self with s inserted at index i."""
        if type(s) == str:
            s = Rope(s)
        # Reduce to concatenation if inserting at either end
        if i == len(self):
            return self + s
        if i == 0:
            return s + self

        left, right = self._cut(i)
        return left + s + right

    def delete(self, i: int, j: int) -> "Rope":
        """Return copy of self with self[i:j] removed."""
        n = len(self)
        if i == 0 and j > n:
            return Rope()
        if i == 0:
            return self._cut(j)[1]
        left, mid = self._cut(i)
        if j > n:
            return left
        mid, right = self._cut(j)
        return left + right

    def _leaves(self) -> Iterator["Rope"]:
        """Iterate over the leaf nodes in order."""
        if self._left:
            yield from self._left._leaves()
        if self._right:
            yield from self._right._leaves()
        if self._text:  # self is a leaf node
            yield self

    def _words(self) -> Iterator[str]:
        """Iterate over the leaf nodes' _text field in order."""
        for leaf in self._leaves():
            yield leaf._text

    def _nodes(self) -> Iterator["Rope"]:
        """Iterate over all nodes in the tree in depth-first, left to right order."""
        if self._left:
            yield from self._left._nodes()
        yield self
        if self._right:
            yield from self._right._nodes()

    def _max_depth(self, depth=0) -> int:
        if self._text:
            return depth + 1
        if self._left:
            left_depth = self._left._max_depth(depth + 1)
        if self._right:
            right_depth = self._right._max_depth(depth + 1)
        return max((left_depth, right_depth))

    def _cut(self, i: int) -> Tuple["Rope", "Rope"]:
        """
        Cut the rope at the point i and return left and right cuts as a tuple.

        Needed for _substring and related operations.
        Rope equivalent of (string[:i], string[i:]).
        """
        if i == 0:
            return Rope(), self
        if i == len(self):
            return self, Rope()
        left_cut = Rope(root=self)
        right_cut = Rope()

        if i >= self._weight and self._right:
            if i == self._weight:
                right_cut = self._right
                left_cut._right = None
                left_cut._len = len(left_cut._left)
                return left_cut, right_cut
            left_cut._right, right_cut = self._right._cut(i - self._weight)
            left_cut._weight = len(left_cut._left)
            left_cut._len = len(left_cut._left) + len(left_cut._right)
            return left_cut, right_cut

        if self._left:
            left_cut._left, right_cut = self._left._cut(i)
            left_cut._right = None
            left_cut._weight = len(left_cut._left)
            left_cut._len = len(left_cut._left)
            if self._right:
                right_cut += self._right
            return left_cut, right_cut

        left_cut, right_cut = Rope(self._text[:i]), Rope(self._text[i:])
        return left_cut, right_cut

    def _substring(self, i: int, j: int) -> "Rope":
        """Implement the substring operation using the _cut() method."""
        n = len(self)
        if not j:
            j = n
        if i == 0 and j > n:
            return Rope(root=self)
        if i == 0:
            return self._cut(j)[0]
        if j > n:
            return self._cut(i)[1]
        left_res = self._cut(j)[0]
        return left_res._cut(i)[1]

    def _rebalance(self) -> "Rope":
        """
        Return a balanced version of self.

        See paper 'Ropes: an alternative to strings' for algorithm description.
        """

        def fib(n) -> int:
            """Return the nth fibonacci number."""
            return ((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5))

        def fibs() -> Iterator[int]:
            """Iterate through the fibonacci sequence."""
            n = 0
            while True:
                yield int(fib(n))
                n += 1

        def balance_slot(n):
            fibs_it = it.takewhile(lambda x: x <= n, fibs())
            return deque(fibs_it, maxlen=1).pop()

        slots: Dict[int, "Rope"] = dict()
        for leaf in self._leaves():
            ln = len(leaf)
            prev = Rope()
            slot = 1
            for slot in it.takewhile(lambda x: x <= ln, fibs()):
                if slot in slots:
                    prev = slots.pop(slot) + prev
            if prev:
                prev += leaf
                slot = balance_slot(len(prev))
                while slot in slots:
                    prev = slots.pop(balance_slot(len(prev))) + prev
                    slot = balance_slot(len(prev))
                slots[slot] = prev
            else:
                slots[slot] = leaf
        result = Rope()
        for slot in sorted(slots):
            result = slots.pop(slot) + result
        return result


if __name__ == "__main__":

    # s = 'Hello world, my name is Jimbo!'
    # r = Rope(s)

    # Test Rope performance against str.
    import string
    import random
    from timer import Timer

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

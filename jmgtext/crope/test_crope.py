"""Unit tests for rope.py."""

# standard library
import itertools as it

# third party

# local module
from jmgtext.crope.crope import Rope

test_str = "Hello world, my name is Jimbo!"


def test_get(rope=Rope(test_str)):
    string = str(rope)
    for i, s in enumerate(string):
        assert rope[i] == s

    # slices = it.combinations(range(len(string)), r=2)
    # for start, stop in slices:
    #     assert rope[start:stop] == string[start:stop]


def test_concat(string=test_str):
    assert Rope(string) * 3 == string * 3
    assert Rope("") * 3 == "" * 3
    for i, _ in enumerate(string):
        left_str, right_str = string[:i], string[i:]
        left_rope, right_rope = Rope(left_str), Rope(right_str)
        concat = left_rope + right_rope
        assert concat == string
        assert len(concat) == len(string)
        test_get(concat)


def test_put(string=test_str):
    text = Rope(string)
    for i, _ in enumerate(string):
        new_text = text.put(i, "--")
        new_string = string[:i] + "--" + string[i:]
        assert new_text == new_string
        test_get(new_text)


def test_delete(string=test_str):
    text = Rope(string)
    slices = it.combinations(range(len(string)), r=2)
    for start, stop in slices:
        assert text.delete(start, stop) == string[:start] + string[stop:]
        test_get(text.delete(start, stop))


def test_logic(string=test_str):
    assert bool(Rope(string)) is bool(string)
    assert bool(Rope("")) is bool("")


if __name__ == "__main__":
    test_get()
    test_concat()
    test_put()
    test_delete()
    test_logic()

    print("All tests passed!")

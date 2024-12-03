import io

from advent.days.day02 import first, is_safe, second

data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def test_first():
    assert first(io.StringIO(data)) == 2


def test_second():
    assert second(io.StringIO(data)) == 4


def test_is_safe():
    assert is_safe([2, 1, 2, 3, 4, 5], 1)
    assert is_safe([1, 2, 3, 4, 5, 2], 1) is True
    assert is_safe([1, 2, 3, 4, 5, 9], 1) is True
    assert is_safe([1, 2, 3, 4, 6, 9], 1) is True
    assert is_safe([1, 6, 3, 4, 6, 9], 1) is True
    assert is_safe([5, 6, 7, 8, 9], 1) is True
    assert is_safe([5, 6, 7, 8, 9, 9], 1) is True
    assert is_safe([5, 6, 7, 7, 9], 1) is True
    assert is_safe([5, 5, 7, 7, 9], 1) is False
    assert is_safe([5, 8, 4, 3], 1) is True

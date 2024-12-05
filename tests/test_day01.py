import io

from advent.days.day01 import first, second

data = """3   4
4   3
2   5
1   3
3   9
3   3"""


def test_first():
    assert first(io.StringIO(data)) == 0


def test_second():
    assert second(io.StringIO(data)) == 31

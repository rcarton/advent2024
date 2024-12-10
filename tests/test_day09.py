import io

from advent.days.day09 import first, second

data = """2333133121414131402"""


def test_first():
    assert first(io.StringIO(data)) == 1928


def test_second():
    assert second(io.StringIO(data)) == 2858

import io

from advent.days.day11 import first, second

data = """125 17"""


def test_first():
    assert first(io.StringIO(data)) == 55312


def test_second():
    assert second(io.StringIO(data)) == 0

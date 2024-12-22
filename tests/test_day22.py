import io

from advent.days.day22 import first, naive, second

data = """1
10
100
2024"""

data_2 = """1
2
3
2024"""


def test_naive():
    assert naive(123, 10) == 5908254


def test_first():
    assert first(io.StringIO(data)) == 37327623


def test_second():
    assert second(io.StringIO(data_2)) == 23

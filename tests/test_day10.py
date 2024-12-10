import io

from advent.days.day10 import first, second

data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def test_first():
    assert first(io.StringIO(data)) == 36


def test_second():
    assert second(io.StringIO(data)) == 81

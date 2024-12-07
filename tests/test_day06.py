import io

from advent.days.day06 import first, second

data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def test_first():
    assert first(io.StringIO(data)) == 41


def test_second():
    assert second(io.StringIO(data)) == 6

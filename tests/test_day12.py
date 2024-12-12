import io

from advent.days.day12 import first, second

data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def test_first():
    assert first(io.StringIO(data)) == 1930


def test_second():
    assert second(io.StringIO(data)) == 1206

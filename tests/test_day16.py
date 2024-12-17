import io

from advent.days.day16 import first, second

data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


data_large = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################"""


def test_first():
    assert first(io.StringIO(data)) == 7036


def test_first_large():
    assert first(io.StringIO(data_large)) == 11048


def test_second():
    assert second(io.StringIO(data)) == 45


def test_second_large():
    assert second(io.StringIO(data_large)) == 64


def test_join():
    d = """#####
#.E.#
##.##
#...#
#.#.#
#.#.#
#...#
##.##
#S..#
#####"""
    assert second(io.StringIO(d)) == 15

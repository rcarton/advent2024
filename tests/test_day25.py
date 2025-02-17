import io

from advent.days.day25 import first, second

data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


def test_first():
    assert first(io.StringIO(data)) == 3


def test_second():
    assert second(io.StringIO(data)) == 0

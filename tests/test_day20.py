import io
from collections import Counter

from advent.days.day20 import Racetrack, first, second

data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def test_first():
    assert first(io.StringIO(data)) == 0


def test_find_all_long_cheats_for_coord():
    m = Racetrack.from_string(data)

    cheats = m.find_all_long_cheats_for_coord(m.start)
    print(cheats)


def test_find_all_long_cheats():
    m = Racetrack.from_string(data)

    cheats = m.find_all_long_cheats(min_saved=50)

    counter = Counter(c[2] for c in cheats)
    assert counter[64] == 19


def test_second():
    assert second(io.StringIO(data)) == 0


def test_nbc_within_distance():
    m = Racetrack.from_string(data)
    nbcs = m.nbc_within_distance(m.start, 3)
    print(nbcs)

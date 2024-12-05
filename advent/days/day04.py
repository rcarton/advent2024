import itertools as it
from typing import TextIO

from advent.matrix import Coord, Matrix
from advent.utils import tadd

Delta = Coord
WordSearch = Matrix


def is_xmas(m: WordSearch, c: Coord, delta: Delta) -> True:
    for letter in "XMAS":
        try:
            if m[c] != letter:
                return False
        except IndexError:
            return False
        c = tadd(c, delta)
    return True


def count_xmas_for_coord(m: WordSearch, c: Coord) -> int:
    directions = list(it.product((-1, 0, 1), repeat=2))
    directions.remove((0, 0))
    return sum(is_xmas(m, c, d) for d in directions)


def is_x_mas(m: WordSearch, c: Coord) -> bool:
    if m[c] != "A":
        return False
    row, col = c
    try:
        return sorted([m[row - 1, col - 1], m[row + 1, col + 1]]) == ["M", "S"] and sorted(
            [m[row + 1, col - 1], m[row - 1, col + 1]]
        ) == ["M", "S"]

    except IndexError:
        return False


def first(input: TextIO) -> int:
    m: WordSearch = Matrix.from_string(input.read())
    return sum(count_xmas_for_coord(m, c) for c in m.all_coords() if m[c] == "X")


def second(input: TextIO) -> int:
    m: WordSearch = Matrix.from_string(input.read())
    return sum(is_x_mas(m, c) for c in m.all_coords())

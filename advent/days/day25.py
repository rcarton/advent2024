import itertools as it
from typing import TextIO

from advent.utils import binseq_to_int

Grid = tuple[int, int, int, int, int]

Lock = Grid
Key = Grid


def parse(s: str) -> tuple[list[Lock], list[Key]]:
    grids_s = s.strip().split("\n\n")

    keys = []
    locks = []

    for grid_s in grids_s:
        grid = zip(*grid_s.split("\n"))
        grid = [binseq_to_int(list(map(lambda c: 1 if c == "#" else 0, line))) for line in grid]

        # If the last bit is set, then it's a key
        is_key = grid[0] & 1

        if is_key:
            keys.append(grid)
        else:
            locks.append(grid)

    return locks, keys


def fit(lock: Lock, key: Key) -> bool:
    return all(l & k == 0 for l, k in zip(lock, key))


def first(input: TextIO) -> int:
    locks, keys = parse(input.read())
    return sum(fit(l, k) for l, k in it.product(locks, keys))


def second(input: TextIO) -> int:
    return -1

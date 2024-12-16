import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Optional, TextIO

from advent.matrix import Coord, Matrix
from advent.utils import mul

Velocity = tuple[int, int]


@dataclass(frozen=True)
class Robot:
    pos: Coord
    velocity: Velocity


def new_position(r: Robot, t: int, nrows: int, ncols: int) -> Coord:
    row, col = r.pos
    drow, dcol = r.velocity

    return (row + t * drow) % nrows, (col + t * dcol) % ncols


def is_in_middle(c: Coord, middle_row: int, middle_col: int) -> bool:
    return c[0] == middle_row or c[1] == middle_col


def get_quadrant(r: Robot, t: int, nrows: int, ncols: int) -> Optional[tuple[int, int]]:
    p = new_position(r, t, nrows, ncols)
    if is_in_middle(p, nrows // 2, ncols // 2):
        return None
    return int(p[0] > nrows // 2), int(p[1] > ncols // 2)


def parse_robot(line: str) -> Robot:
    col, row, dcol, drow = [int(n) for n in re.findall(r"-?\d+", line)]
    return Robot((row, col), (drow, dcol))


def iterate(robots: list[Robot], total_t: int, nrows: int, ncols: int) -> int:
    m = Matrix(["."] * nrows * ncols, ncols, nrows)
    for t in range(total_t):
        positions = defaultdict(int)
        for r in robots:
            positions[new_position(r, t + 1, nrows, ncols)] += 1

        # I guess they should all be 1?
        if max(positions.values()) > 1:
            continue

        for c, v in positions.items():
            m[c] = str(v)
        print(f"\nt={t+1}")
        print(m)

        return t + 1
        # Reset if displaying more than once
        # m.data = ['.'] * nrows * ncols


def first(input: TextIO, nrows: int = 103, ncols=101, t: int = 100) -> int:
    robots = [parse_robot(l) for l in input.readlines()]

    # iterate(robots, t, nrows, ncols)

    robots_per_quadrant = Counter(get_quadrant(r, t, nrows, ncols) for r in robots)
    return mul(count for quadrant, count in robots_per_quadrant.items() if quadrant is not None)


def second(input: TextIO, nrows: int = 103, ncols=101, t: int = 10000) -> int:
    robots = [parse_robot(l) for l in input.readlines()]
    return iterate(robots, t, nrows, ncols)

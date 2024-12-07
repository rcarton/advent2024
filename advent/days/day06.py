import itertools as it
from typing import Optional, TextIO

from advent.matrix import Coord, Direction, Matrix
from advent.utils import tadd

Map = Matrix[str]

Delta = tuple[int, int]
ORIENTATIONS: list[Direction] = ["up", "right", "down", "left"]

MOVE_DELTAS: dict[Direction, Delta] = {
    "up": (-1, 0),
    "right": (0, 1),
    "down": (1, 0),
    "left": (0, -1),
}


def moves(
    m: Map,
    starting: Optional[Coord] = None,
    direction: Optional[Direction] = None,
    block: Optional[Coord] = None,
) -> tuple[set[Coord], bool]:
    if starting is None:
        gp = [c for c in m.all_coords() if m[c] == "^"][0]
    else:
        gp = starting

    i_dir = it.cycle(ORIENTATIONS)
    if direction is None:
        gd = next(i_dir)
    else:
        gd = direction
        while next(i_dir) != direction:
            pass

    all_positions = set()
    seen = set()

    while True:
        all_positions.add(gp)
        if (gp, gd) in seen:
            return all_positions, False
        seen.add((gp, gd))

        next_position = tadd(gp, MOVE_DELTAS[gd])

        if not m.is_valid_coord(next_position):
            return all_positions, True

        if next_position == block or m[next_position] == "#":
            # Turn
            gd = next(i_dir)
            continue

        gp = next_position


def count_loops(m: Map) -> int:
    i_dir = it.cycle(ORIENTATIONS)
    gp = [c for c in m.all_coords() if m[c] == "^"][0]
    gd = next(i_dir)

    total_loops = 0

    visited = {gp}

    while True:
        visited.add(gp)
        next_position = tadd(gp, MOVE_DELTAS[gd])

        if not m.is_valid_coord(next_position):
            return total_loops

        if m[next_position] == "#":
            # Turn
            gd = next(i_dir)
            continue

        # Add a block in the next position and see if this would create a loop
        if next_position not in visited and is_looping(m, gp, gd, next_position):
            total_loops += 1

        gp = next_position


def is_looping(m: Map, starting: Coord, direction: Direction, block: Coord) -> bool:
    _, completes = moves(m, starting, direction, block)
    return not completes


def first(input: TextIO) -> int:
    m = Matrix.from_string(input.read())
    positions, completed = moves(m)
    assert completed is True
    return len(positions)


def second(input: TextIO) -> int:
    m = Matrix.from_string(input.read())
    return count_loops(m)

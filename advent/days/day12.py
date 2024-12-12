from collections import deque
from typing import TextIO

from advent.matrix import Coord, Matrix
from advent.utils import tadd

Farm = Matrix[str]


def visit_area(f: Farm, c: Coord, visited: set[Coord]) -> tuple[int, int, int]:
    # Type of plot we're looking for
    v = f[c]

    coords_in_area = set()
    to_visit = deque([c])
    while to_visit:
        curr = to_visit.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        coords_in_area.add(curr)

        # Now look for neighbors
        for nc in f.nbc4(curr):
            nv = f[nc]
            if nv != v or nc in visited:
                continue
            to_visit.append(nc)

    surface_area = len(coords_in_area)
    perimeter = sum(4 - sum(nv == v for nv in f.neighbors(cc)) for cc in coords_in_area)

    # Count the sides
    side_ds = {
        "up": (-1, 0),
        "right": (0, 1),
        "down": (1, 0),
        "left": (0, -1),
    }

    def is_perim(c: Coord, side: str) -> bool:
        nc = tadd(c, side_ds[side])
        return f.get(nc) != v

    known_sides = set()
    side_count = 0
    for c in coords_in_area:
        # For each side of the coord, we check if it's a perimeter, add 1 to the side count, and explore the rest of
        # that side
        for side in side_ds.keys():
            if not is_perim(c, side) or (c, side) in known_sides:
                continue

            # We have found an unexplored side, add 1 then explore it in both directions
            known_sides.add((c, side))
            side_count += 1

            # go in both directions to try to continue the sides
            deltas = ((0, 1), (0, -1)) if side in ("up", "down") else ((-1, 0), (1, 0))
            for d in deltas:
                curr = tadd(c, d)
                while f.get(curr) == v and is_perim(curr, side):
                    known_sides.add((curr, side))
                    curr = tadd(curr, d)

    return surface_area, perimeter, side_count


def first(input: TextIO) -> int:
    farm = Matrix.from_string(input.read())
    visited = set()

    price = 0
    for c in farm.all_coords():
        if c in visited:
            continue
        area, perimeter, _ = visit_area(farm, c, visited)
        price += area * perimeter

    return price


def second(input: TextIO) -> int:
    farm = Matrix.from_string(input.read())
    visited = set()

    price = 0
    for c in farm.all_coords():
        if c in visited:
            continue
        area, _, side_count = visit_area(farm, c, visited)
        price += area * side_count

    return price

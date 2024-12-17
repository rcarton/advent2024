import math
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import TextIO

from advent.matrix import DIR_DELTAS, Coord, Direction, Matrix
from advent.utils import tadd

Maze = Matrix[str]


@dataclass(order=True)
class Candidate:
    cost: int
    dir: Direction
    coord: Coord
    # In any path that ends up at this cost, coord, and direction
    in_path: set[Coord]


@dataclass(order=True)
class Candidate2:
    cost: int
    dir: Direction
    coord: Coord
    # In any path that ends up at this cost, coord, and direction
    path: list[Coord]


def find_solutions(m: Maze) -> list[Candidate]:
    start = next(iter(c for c, v in m.items() if v == "S"))
    end = next(iter(c for c, v in m.items() if v == "E"))

    candidates: list[Candidate] = []
    existing_candidates: dict[tuple[Direction, Coord], Candidate] = {}
    heappush(candidates, Candidate(0, "right", start, {start}))
    visited: set[tuple[Direction, Coord]] = set()

    min_cost = None
    solutions: list[Candidate] = []

    while candidates:
        curr = heappop(candidates)

        if min_cost and curr.cost > min_cost:
            # Too expensive
            continue

        if curr.coord == end:
            solutions.append(curr)
            min_cost = curr.cost
            continue

        if (curr.dir, curr.coord) in visited:
            continue
        visited.add((curr.dir, curr.coord))

        # If we keep going
        c = tadd(curr.coord, DIR_DELTAS[curr.dir])
        next_cost = curr.cost + 1
        next_dir_coord = (curr.dir, c)
        if m[c] != "#" and next_dir_coord not in visited:
            if next_dir_coord in existing_candidates:
                if next_cost == existing_candidates[next_dir_coord].cost:
                    # Merge the paths
                    existing_candidates[next_dir_coord].in_path |= curr.in_path
            else:
                candidate = Candidate(next_cost, curr.dir, c, curr.in_path | {c})
                heappush(candidates, candidate)
                existing_candidates[next_dir_coord] = candidate

        # Now the turns
        other_dirs: tuple[Direction] = (
            ("left", "right") if curr.dir in ("up", "down") else ("up", "down")
        )
        for dir in other_dirs:
            next_cost = curr.cost + 1000
            next_dir_coord = (dir, curr.coord)

            if next_dir_coord in existing_candidates:
                if next_cost == existing_candidates[next_dir_coord].cost:
                    # Merge the paths
                    existing_candidates[next_dir_coord].in_path |= curr.in_path
            else:
                candidate = Candidate(next_cost, dir, curr.coord, curr.in_path)
                heappush(candidates, candidate)
                existing_candidates[next_dir_coord] = candidate

    return solutions


def find_all_solutions(m: Maze) -> list[Candidate2]:
    """This is less elegant than the first solution, but there must be some broken logic in the merge logic because
    it finds 4 extra positions over the second one.
    """
    start = next(iter(c for c, v in m.items() if v == "S"))
    end = next(iter(c for c, v in m.items() if v == "E"))

    candidates: list[Candidate2] = []
    heappush(candidates, Candidate2(0, "right", start, [start]))
    visited: dict[tuple[Direction, Coord], int] = {}

    min_cost = None
    solutions: list[Candidate2] = []

    while candidates:
        curr = heappop(candidates)

        if min_cost and curr.cost > min_cost:
            # Too expensive
            continue

        if curr.coord == end:
            solutions.append(curr)
            min_cost = curr.cost
            continue

        if curr.cost > visited.get((curr.dir, curr.coord), math.inf):
            continue
        visited[(curr.dir, curr.coord)] = curr.cost

        # If we keep going
        c = tadd(curr.coord, DIR_DELTAS[curr.dir])
        next_cost = curr.cost + 1
        next_dir_coord = (curr.dir, c)
        if m[c] != "#" and next_cost <= visited.get(next_dir_coord, math.inf):
            candidate = Candidate2(next_cost, curr.dir, c, curr.path + [c])
            heappush(candidates, candidate)

        # Now the turns
        other_dirs: tuple[Direction] = (
            ("left", "right") if curr.dir in ("up", "down") else ("up", "down")
        )
        for dir in other_dirs:
            next_cost = curr.cost + 1000
            next_dir_coord = (dir, curr.coord)
            if next_dir_coord and next_cost <= visited.get(next_dir_coord, math.inf):
                candidate = Candidate2(next_cost, dir, curr.coord, curr.path)
                heappush(candidates, candidate)

    return solutions


def first(input: TextIO) -> int:
    maze = Matrix.from_string(input.read())
    solutions = find_solutions(maze)
    return solutions[0].cost


def second(input: TextIO) -> int:
    maze = Matrix.from_string(input.read())
    solutions = find_all_solutions(maze)

    start = next(iter(c for c, v in maze.items() if v == "S"))
    end = next(iter(c for c, v in maze.items() if v == "E"))

    good_seats: set[Coord] = {start, end}
    for solution in solutions:
        good_seats |= set(solution.path)

    # 552 was too high
    return len(good_seats)

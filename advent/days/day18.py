from typing import TextIO

from advent.matrix import Coord, Matrix

Byte = tuple[int, int]
Memory = Matrix[str]


def find_shortest_path(mem: Memory) -> int:
    s: Coord = (0, 0)
    e: Coord = (mem.width - 1, mem.height - 1)

    count = 0
    to_explore = {s}
    visited = set()
    while to_explore:
        new_to_explore = set()

        for c in to_explore:
            if c in visited:
                continue

            visited.add(c)
            if c == e:
                return count
            for nc in mem.nbc4(c):
                v = mem[nc]
                if v == ".":
                    new_to_explore.add(nc)

        count += 1
        to_explore = new_to_explore

    raise ValueError("Path not found")


def first(input: TextIO, size: int = 71, time: int = 1024) -> int:
    # Reversing to be row, col instead of col, row
    bytes: list[Byte] = [tuple(reversed(list(map(int, l.split(","))))) for l in input.readlines()]
    mem = Matrix(["."] * size * size, size, size)

    # Drop the bytes
    it_bytes = iter(bytes)
    for t in range(time):
        c = next(it_bytes)
        mem[c] = "#"

    return find_shortest_path(mem)


def second(input: TextIO, size: int = 71) -> str:
    bytes: list[Byte] = [tuple(reversed(list(map(int, l.split(","))))) for l in input.readlines()]
    mem = Matrix(["."] * size * size, size, size)

    # Drop the bytes
    for t, c in enumerate(bytes):
        # t is actually t-1
        mem[c] = "#"
        try:
            find_shortest_path(mem)
        except ValueError:
            return f"{c[1]},{c[0]}"

    # This is bruteforcey, but the map is small so it's fine, otherwise we could do some binary search to narrow down
    # the t, and then we could make a graph with all the paths and look at the vertices with the lowest t (t = drop time)
    raise ValueError("blocking byte not found")

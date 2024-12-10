from collections import defaultdict, deque
from typing import Deque, TextIO

from advent.matrix import Coord, Matrix


def first(input: TextIO) -> int:
    map = Matrix.from_string(input.read(), int)

    # Compute scores to get there, the score for a Coord with value n is the sum of scores of all the n+1
    scores: dict[Coord, set] = defaultdict(set)
    to_visit: set[Coord] = set()
    for c, v in map.items():
        if v == 9:
            scores[c].add(c)
            to_visit |= {nc for nc in map.nbc4(c) if map[nc] == v - 1}

    while to_visit:
        c = to_visit.pop()
        v = map[c]

        for nc in map.nbc4(c):
            if map[nc] == v + 1:
                scores[c] |= scores[nc]
            if map[nc] == v - 1:
                to_visit.add(nc)

    return sum(len(scores[c]) for c, v in map.items() if v == 0)


def second(input: TextIO) -> int:
    map = Matrix.from_string(input.read(), int)

    # Compute scores to get there, the score for a Coord with value n is the sum of scores of all the n+1
    scores: dict[Coord, int] = defaultdict(int)
    to_visit: Deque[Coord] = deque()
    visited: set[Coord] = set()
    for c, v in map.items():
        if v == 9:
            scores[c] = 1
            to_visit.extend(nc for nc in map.nbc4(c) if map[nc] == v - 1)

    while to_visit:
        c = to_visit.popleft()
        if c in visited:
            continue
        visited.add(c)
        v = map[c]

        for nc in map.nbc4(c):
            if map[nc] == v + 1:
                scores[c] += scores[nc]
            if map[nc] == v - 1:
                to_visit.append(nc)

    return sum(scores[c] for c, v in map.items() if v == 0)

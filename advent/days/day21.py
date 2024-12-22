import itertools as it
import re
from collections import defaultdict, deque
from functools import cache
from typing import TextIO

from advent.matrix import Matrix
from advent.utils import tadd

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+


    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

🧍🏼AKP -> 🤖 AKP -> 🤖 AKP -> 🤖 KP
"""

NUM_GRID = """789
456
123
#0A"""

ARROW_GRID = """#^A
<v>"""

Combo = str
FromTo = tuple[str, str]


def precompute_combos(grid: str) -> dict[FromTo, list[Combo]]:
    num_combos = defaultdict(list)
    num_matrix = Matrix.from_string(grid)

    deltas = {
        "<": (0, -1),
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
    }

    for start, v in num_matrix.items():
        if v == "#":
            continue

        num_combos[(v, v)].append("")

        to_visit = deque([("", start)])
        while to_visit:
            path, c = to_visit.popleft()
            for arrow, d in deltas.items():
                nc = tadd(c, d)
                n = num_matrix.get(nc)
                if n is None or n == "#" or n == v:
                    continue
                new_path = path + arrow

                # Ignore alternating patterns
                if re.match(r".*(.)(?:(?!\1).)+\1.*", new_path):
                    continue

                # Ignore if longer
                if len(num_combos[(v, n)]) > 0 and len(new_path) > len(num_combos[(v, n)][0]):
                    continue

                num_combos[(v, n)].append(new_path)
                to_visit.append((new_path, nc))

    return num_combos


NUM_COMBOS: dict[FromTo, list[Combo]] = precompute_combos(NUM_GRID)
ARROW_COMBOS: dict[FromTo, list[Combo]] = precompute_combos(ARROW_GRID)


@cache
def min_presses_path(path: str, depth: int) -> int:
    return sum(min_presses_key(fr, to, depth) for fr, to in it.pairwise("A" + path))


@cache
def min_presses_key(fr: str, to: str, depth: int) -> int:
    if depth == 0:
        return 1

    return min(min_presses_path(p + "A", depth - 1) for p in ARROW_COMBOS[(fr, to)])


def all_paths(path: str, depth: int) -> list[Combo]:
    if depth == 0:
        return [path]

    paths = [""]
    for fr, to in it.pairwise("A" + path):
        curr_paths = [c + "A" for c in ARROW_COMBOS[(fr, to)]]
        paths = ["".join(l) for l in it.product(paths, curr_paths)]

    return list(it.chain(*[all_paths(p, depth - 1) for p in paths]))


def min_button_presses_for_code(code: str, depth: int = 2) -> int:
    # A code is a numpad code, a path is a code for the arrow pad, so we're turning the code into possible paths
    # then solving for each path and keeping the minimum.
    prev = "A"
    paths = [""]
    for curr in code:
        curr_paths = [c + "A" for c in NUM_COMBOS[(prev, curr)]]
        paths = ["".join(l) for l in it.product(paths, curr_paths)]
        prev = curr

    return min(min_presses_path(p, depth) for p in paths)


def complexity(code: str, depth: int = 2) -> int:
    return min_button_presses_for_code(code, depth) * int(re.findall(r"\d+", code)[0])


def first(input: TextIO) -> int:
    return sum(complexity(code.strip()) for code in input.readlines())


def second(input: TextIO) -> int:
    return sum(complexity(code.strip(), 25) for code in input.readlines())

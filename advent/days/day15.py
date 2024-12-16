from collections import deque
from typing import Literal, TextIO

from advent.matrix import Coord, Delta, Matrix, T
from advent.utils import tadd, tsub

Direction = Literal["^", "v", "<", ">"]

DELTAS: dict[Direction, Delta] = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


class Warehouse(Matrix[str]):
    robot_c: Coord
    has_big_boxes: bool

    @classmethod
    def from_string(cls, data: str, double: bool = True) -> "Warehouse[T]":
        if double:
            data = data.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")

        w = super(cls, cls).from_string(data, None)
        w.robot_c = next(iter(c for c, v in w.items() if v == "@"))
        w.has_big_boxes = any(v == "[" for v in data)
        return w

    def move(self, dir: Direction) -> None:
        if not self.has_big_boxes or dir in (">", "<"):
            self.move_h(dir)
        else:
            self.move_v(dir)

    def move_v(self, dir: Direction) -> None:
        candidates_to_move = deque([self.robot_c])
        moves_to_apply = deque([])
        candidates_considered = set()
        while candidates_to_move:
            c = candidates_to_move.popleft()
            if c in candidates_considered:
                continue
            candidates_considered.add(c)
            to = tadd(c, DELTAS[dir])
            v = self[to]
            if v == "#":
                # We've hit a wall for one of the candidates, we can't move at all
                return

            moves_to_apply.append((c, to))

            if v == ".":
                continue
            if v == "[":
                candidates_to_move.append(to)
                candidates_to_move.append((to[0], to[1] + 1))
            if v == "]":
                candidates_to_move.append((to[0], to[1] - 1))
                candidates_to_move.append(to)

        # Apply all the moves starting from the latest
        while moves_to_apply:
            fr, to = moves_to_apply.pop()
            self[to] = self[fr]
            self[fr] = "."

            if self[to] == "@":
                self.robot_c = to

    def move_h(self, dir: Direction) -> None:
        curr = tadd(self.robot_c, DELTAS[dir])

        # Find the coordinate of the next non box
        while True:
            v = self[curr]
            if v == "#":
                # Can't move, we hit a wall
                return
            if v == ".":
                break
            # Otherwise it's a box, keep going
            curr = tadd(curr, DELTAS[dir])

        # Scoot everything
        while True:
            prev = tsub(curr, DELTAS[dir])
            self[curr], self[prev] = self[prev], self[curr]
            if prev == self.robot_c:
                self.robot_c = curr
                break
            curr = prev

    def score(self) -> int:
        return sum(100 * row + col for (row, col), v in self.items() if v in ("O", "["))


def first(input: TextIO) -> int:
    w_s, moves_s = input.read().strip().split("\n\n")

    w = Warehouse.from_string(w_s, False)

    for dir in moves_s:
        if dir == "\n":
            continue
        w.move(dir)
        # print()
        # print(w)

    return w.score()


def second(input: TextIO) -> int:
    w_s, moves_s = input.read().strip().split("\n\n")

    w = Warehouse.from_string(w_s)

    print()
    print(w)
    for dir in moves_s:
        if dir == "\n":
            continue
        w.move(dir)
        # print()
        # print(dir)
        # print()
        # print(w)

    return w.score()

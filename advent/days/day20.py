from typing import TextIO

from advent.matrix import Coord, Matrix, manhattan_distance

Cheat = tuple[Coord, Coord, int]
CheatPair: tuple[Coord, Coord]


class Racetrack(Matrix[str]):
    start: Coord
    end: Coord

    distances: dict[Coord, int | None]

    @classmethod
    def from_string(cls, data: str, fn=None) -> "Racetrack":
        rt = super(cls, cls).from_string(data, fn)
        start = end = None
        for c, v in rt.items():
            if start and end:
                break
            if v == "S":
                rt.start = c
            elif v == "E":
                rt.end = c
        rt.compute_distances()
        return rt

    def compute_distances(self) -> None:
        self.distances = {}
        visited = set()
        curr = self.start
        self.distances[self.start] = 0
        count = 0
        while True:
            visited.add(curr)
            count += 1
            for nc in self.nbc4(curr):
                if nc not in visited and self[nc] != "#":
                    curr = nc
                    break
            self.distances[curr] = count
            if curr == self.end:
                break

    def find_all_long_cheats(self, max_cheat_time: int = 20, min_saved: int = 0) -> list[Cheat]:
        cheats = []
        for _, c in sorted((d, c) for c, d in self.distances.items()):
            cheats.extend(self.find_all_long_cheats_for_coord(c, max_cheat_time, min_saved))
        return cheats

    def find_all_long_cheats_for_coord(
        self, c: Coord, max_cheat_time: int = 20, min_saved: int = 0
    ) -> list[Cheat]:
        cheats = []
        unique_cheats = set()
        for nc in self.nbc_within_distance(c, max_cheat_time):
            nv = self[nc]
            distance = manhattan_distance(c, nc)
            if nv != "#":
                d1 = self.distances[c]
                d2 = self.distances[nc]

                time_saving = d2 - d1 - distance

                pair = (c, nc)
                if time_saving >= min_saved and pair not in unique_cheats:
                    unique_cheats.add(pair)
                    cheats.append((c, nc, time_saving))
        return cheats


def first(input: TextIO) -> int:
    m = Racetrack.from_string(input.read())
    cheats = m.find_all_long_cheats(max_cheat_time=2, min_saved=100)
    return len(cheats)


def second(input: TextIO) -> int:
    m = Racetrack.from_string(input.read())
    cheats = m.find_all_long_cheats(min_saved=100)
    return len(cheats)

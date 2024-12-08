import itertools as it
import re
from collections import defaultdict
from typing import TextIO

from advent.matrix import Coord, Matrix
from advent.utils import tadd, tsub

AntennaMap = dict[str, list[Coord]]
Map = Matrix[str]


def get_antinodes_for_pair(map: Map, c1: Coord, c2: Coord) -> set[Coord]:
    delta = c2[0] - c1[0], c2[1] - c1[1]
    antinodes = set()

    a1 = tsub(c1, delta)
    a2 = tadd(c2, delta)

    for a in (a1, a2):
        if map.is_valid_coord(a):
            antinodes.add(a)

    return antinodes


def get_antinodes_for_pair_v2(map: Map, c1: Coord, c2: Coord) -> set[Coord]:
    delta = c2[0] - c1[0], c2[1] - c1[1]
    antinodes = {c1}

    curr = tsub(c1, delta)
    while map.is_valid_coord(curr):
        antinodes.add(curr)
        curr = tsub(curr, delta)

    curr = tadd(c1, delta)
    while map.is_valid_coord(curr):
        antinodes.add(curr)
        curr = tadd(curr, delta)

    return antinodes


def get_antinodes_for_list(map: Map, antennas: list[Coord], v2: bool = False) -> set[Coord]:
    nodes = set()

    for c1, c2 in it.combinations(antennas, 2):
        if not v2:
            nodes |= get_antinodes_for_pair(map, c1, c2)
        else:
            nodes |= get_antinodes_for_pair_v2(map, c1, c2)

    return nodes


def first(input: TextIO) -> int:
    map = Matrix.from_string(input.read())
    antenna_map: AntennaMap = defaultdict(list)

    for c, v in map.items():
        if re.match(r"[\w\d]", v):
            antenna_map[v].append(c)

    antinodes = set()
    for antennas_coords in antenna_map.values():
        antinodes |= get_antinodes_for_list(map, antennas_coords)

    return len(antinodes)


def second(input: TextIO) -> int:
    map = Matrix.from_string(input.read())
    antenna_map: AntennaMap = defaultdict(list)

    for c, v in map.items():
        if re.match(r"[\w\d]", v):
            antenna_map[v].append(c)

    antinodes = set()
    for antennas_coords in antenna_map.values():
        antinodes |= get_antinodes_for_list(map, antennas_coords, True)

    return len(antinodes)

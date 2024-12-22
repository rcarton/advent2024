import itertools as it
from collections import defaultdict
from typing import TextIO

Network = dict[str, set[str]]


def first(input: TextIO) -> int:
    lines = input.readlines()
    network: Network = defaultdict(set)
    for line in lines:
        c1, c2 = line.strip().split("-")
        network[c1].add(c2)
        network[c2].add(c1)

    # List of computers that start with a t
    start_with_t = [k for k in network.keys() if k[0] == "t"]

    # Groups are pairs of 2 that both have each other in their networks
    groups = set()
    for computer in start_with_t:
        for p1, p2 in it.combinations(network[computer], 2):
            if p2 in network[p1]:
                groups.add(tuple(sorted([computer, p1, p2])))

    return len(groups)


def second(input: TextIO) -> str:
    lines = input.readlines()
    network: Network = defaultdict(set)
    for line in lines:
        c1, c2 = line.strip().split("-")
        network[c1].add(c2)
        network[c2].add(c1)

    largest_combos = set()

    for c in network.keys():
        combo_found = None
        for l in range(len(network[c]) - 1, 0, -1):
            for combo in it.combinations(network[c], l):
                # The combo is valid if they're all
                works = all((set(combo) - {cc}) <= network[cc] for cc in combo)

                if works:
                    combo_found = tuple(sorted(set(combo) | {c}))
                    break
            if combo_found:
                break

        if combo_found:
            largest_combos.add(combo_found)

    largest_combos = sorted(largest_combos, key=lambda c: len(c), reverse=True)

    return ",".join(largest_combos[0])

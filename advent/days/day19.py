from functools import cache
from typing import TextIO

Towel = str
Towels = set[Towel]


def first(input: TextIO) -> int:
    towels_s, patterns_s = input.read().split("\n\n")
    towels = set(towels_s.split(", "))
    patterns = patterns_s.strip().split("\n")

    @cache
    def has_solution(pattern: str) -> bool:
        if len(pattern) == 0:
            return True
        return any(has_solution(pattern[len(t) :]) for t in towels if pattern.startswith(t))

    return sum(has_solution(p) for p in patterns)


def second(input: TextIO) -> int:
    towels_s, patterns_s = input.read().split("\n\n")
    towels = set(towels_s.split(", "))
    patterns = patterns_s.strip().split("\n")

    @cache
    def all_solutions(pattern: str) -> int:
        if len(pattern) == 0:
            return 1
        return sum(all_solutions(pattern[len(t) :]) for t in towels if pattern.startswith(t))

    return sum(all_solutions(p) for p in patterns)

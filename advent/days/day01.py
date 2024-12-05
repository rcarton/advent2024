from collections import Counter
from typing import TextIO


def first(input: TextIO) -> int:
    left, right = zip(*list(map(int, l.split("   ")) for l in input.readlines()))
    left, right = sorted(left), sorted(right)
    return sum(abs(a - b) for a, b in zip(left, right))


def second(input: TextIO) -> int:
    left, right = zip(*list(map(int, l.split("   ")) for l in input.readlines()))
    cnt = Counter(right)
    return sum(a * cnt[a] for a in left)

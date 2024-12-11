from functools import cache
from typing import TextIO


def blink(n: int) -> list[int]:
    if n == 0:
        return [1]
    ns = str(n)
    if len(ns) % 2 == 0:
        half = len(ns) // 2
        return [int(ns[:half]), int(ns[half:])]
    return [n * 2024]


@cache
def blink_times_total_stones(stone: int, times: int) -> int:
    if times == 0:
        return 1
    return sum(blink_times_total_stones(s, times - 1) for s in blink(stone))


def first(input: TextIO) -> int:
    stones = [int(s) for s in input.read().strip().split(" ")]
    return sum(blink_times_total_stones(s, 25) for s in stones)


def second(input: TextIO) -> int:
    stones = [int(s) for s in input.read().strip().split(" ")]
    return sum(blink_times_total_stones(s, 75) for s in stones)

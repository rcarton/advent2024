from typing import Optional, Set, TextIO


def naive(secret_number: int, times: Optional[int] = 2000) -> int:
    n = secret_number
    for _ in range(times):
        n = ((n * 64) ^ n) % 16777216
        n = ((n // 32) ^ n) % 16777216
        n = ((n * 2048) ^ n) % 16777216

    return n


Seq = tuple[int, int, int, int]


def find_max_bananas(
    secret_number: int, bananarama: dict[Seq, int], times: Optional[int] = 2000
) -> None:
    n = secret_number
    seen: Set[Seq] = set()
    prev_value = None
    seq = tuple()
    for _ in range(times):
        n = ((n * 64) ^ n) % 16777216
        n = ((n // 32) ^ n) % 16777216
        n = ((n * 2048) ^ n) % 16777216

        banana_count = n % 10
        if prev_value is None:
            prev_value = banana_count
            continue

        diff = n % 10 - prev_value
        seq = tuple(seq[-3:] + (diff,))

        if len(seq) == 4:
            if seq not in seen:
                bananarama[seq] = bananarama.get(seq, 0) + banana_count
            seen.add(seq)
        prev_value = n % 10


def first(input: TextIO) -> int:
    nums = [int(n) for n in input.readlines()]
    return sum(naive(n) for n in nums)


def second(input: TextIO) -> int:
    nums = [int(n) for n in input.readlines()]
    bananarama = {}

    for n in nums:
        find_max_bananas(n, bananarama)
    return max(bananarama.values())

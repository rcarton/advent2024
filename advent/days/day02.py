import itertools as it
from typing import TextIO


def is_safe(report: list[int], skips_left: int = 1) -> bool:
    increase = None

    for ea, eb in it.pairwise(enumerate(report)):
        ia, a = ea
        ib, b = eb

        def fallback():
            if skips_left == 0:
                return False

            report_a = report[:ia] + report[ia + 1:] if ia > 0 else report[ia + 1:]
            report_b = report[:ib] + report[ib + 1:]

            if ia == 0:
                return is_safe(report[1:], skips_left - 1) or is_safe(report[:1] + report[1 + 1:], skips_left - 1)
            elif ia == 1:
                return (is_safe(report[1:], skips_left - 1) or is_safe(report_a, skips_left - 1) or is_safe(report_b,
                                                                                                            skips_left - 1))
            else:
                return is_safe(report_a, skips_left - 1) or is_safe(report_b, skips_left - 1)

        if a == b:
            return fallback()

        if increase is None:
            increase = True if b > a else False

        if increase and b < a:
            return fallback()
        elif increase is False and b > a:
            return fallback()

        if abs(b - a) > 3:
            return fallback()

    return True


def first(input: TextIO) -> int:
    reports = [list(map(int, l.split(' '))) for l in input.readlines()]
    return sum(is_safe(r, 0) for r in reports)


def second(input: TextIO) -> int:
    reports = [list(map(int, l.split(' '))) for l in input.readlines()]
    return sum(is_safe(r) for r in reports)

from typing import TextIO

Eq = tuple[int, list[int]]


def parse_operation(line: str) -> Eq:
    left, right = line.split(": ")
    result = int(left)
    numbers = [int(n) for n in right.split(" ")]
    return result, numbers


def concat(n1: int, n2: int) -> int:
    return int(str(n1) + str(n2))


def is_valid(eq: Eq, allow_concat: bool = False) -> bool:
    possibles = set()
    result, numbers = eq

    for i, n in enumerate(numbers):
        is_last = i == len(numbers) - 1
        if not possibles:
            possibles.add(n)
            continue

        new_possibles = set()
        for p in possibles:
            if p * n <= result:
                new_possibles.add(p * n)
            if p + n <= result:
                new_possibles.add(p + n)

            if allow_concat and (concatenated := concat(p, n)) <= result:
                new_possibles.add(concatenated)

        if is_last and result in new_possibles:
            return True

        possibles = new_possibles

    return False


def first(input: TextIO) -> int:
    eqs_str = input.readlines()
    eqs = [parse_operation(eq) for eq in eqs_str]
    return sum(eq[0] for eq in eqs if is_valid(eq))


def second(input: TextIO) -> int:
    eqs_str = input.readlines()
    eqs = [parse_operation(eq) for eq in eqs_str]
    return sum(eq[0] for eq in eqs if is_valid(eq, True))

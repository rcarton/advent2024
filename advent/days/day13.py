import re
from dataclasses import dataclass
from typing import Optional, TextIO

from sympy import Float, Matrix


@dataclass(frozen=True)
class Claw:
    a: tuple[int, int]
    b: tuple[int, int]
    prize: tuple[int, int]


def parse_claw(claw_str: str, prize_adjustment: int = 0) -> Claw:
    a_x, a_y, b_x, b_y, prize_x, prize_y = [int(n) for n in re.findall(r"\d+", claw_str)]
    return Claw(
        a=(a_x, a_y),
        b=(b_x, b_y),
        prize=(prize_x + prize_adjustment, prize_y + prize_adjustment),
    )


def resolve_claw(claw: Claw) -> Optional[tuple[int, int]]:
    """Return the number of presses of A, B, None if no solutions"""
    m = Matrix([[claw.a[i], claw.b[i]] for i in (0, 1)])

    try:
        sol, params = m.gauss_jordan_solve(Matrix(list(claw.prize)))
    except ValueError:
        return None
    sol_unique = sol.xreplace({tau: 0 for tau in params})
    if any(Float(n) % 1 != 0 for n in sol_unique):
        return None
    return int(sol_unique[0]), int(sol_unique[1])


def first(input: TextIO) -> int:
    claws = [parse_claw(c) for c in input.read().split("\n\n")]
    return sum(3 * cost[0] + cost[1] for c in claws if (cost := resolve_claw(c)) is not None)


def second(input: TextIO) -> int:
    claws = [parse_claw(c, prize_adjustment=10000000000000) for c in input.read().split("\n\n")]
    return sum(3 * cost[0] + cost[1] for c in claws if (cost := resolve_claw(c)) is not None)

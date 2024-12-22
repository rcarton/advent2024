import re
from collections import deque
from dataclasses import dataclass
from typing import Literal, TextIO

from advent.utils import binseq_to_int

State = dict[str, None | Literal[0, 1]]


@dataclass(frozen=True)
class Gate:
    op: Literal["AND", "OR", "XOR"]
    left: str
    right: str
    out: str


def first(input: TextIO) -> int:
    init_str, circuit_str = input.read().split("\n\n")

    state = {}
    for line in init_str.split("\n"):
        wire, value = line.split(": ")
        state[wire] = int(value)

    gates = []
    for line in circuit_str.strip().split("\n"):
        left, op, right, out = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", line).groups()
        gates.append(Gate(op=op, left=left, right=right, out=out))

    todo = deque(gates)
    while todo:
        g = todo.popleft()
        lv = state.get(g.left, None)
        rv = state.get(g.right, None)
        if lv is None or rv is None:
            todo.append(g)
            continue

        if g.op == "AND":
            ov = lv & rv
        elif g.op == "OR":
            ov = lv | rv
        elif g.op == "XOR":
            ov = lv ^ rv
        else:
            raise ValueError("Unknown op.")
        state[g.out] = ov

    # Get all the wires starting with z
    z_keys = sorted([k for k in state.keys() if k.startswith("z")], reverse=True)
    z_values = [state[k] for k in z_keys]

    return binseq_to_int(z_values)


def second(input: TextIO) -> int:
    init_str, circuit_str = input.read().split("\n\n")

    state = {}
    for line in init_str.split("\n"):
        wire, value = line.split(": ")
        state[wire] = int(value)

    gates = []
    for line in circuit_str.strip().split("\n"):
        left, op, right, out = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", line).groups()
        gates.append(Gate(op=op, left=left, right=right, out=out))
        state[left] = 0
        state[right] = 0
        state[out] = 0

    def get_num(var: str) -> int:
        z_keys = sorted([k for k in state.keys() if k.startswith(var)], reverse=True)
        z_values = [state[k] for k in z_keys]
        return binseq_to_int(z_values)

    x = get_num("x")
    y = get_num("y")
    print(f"x={x}, y={y}, expected z={x+y}")

    # Sort the gates
    new_gates = []
    for g in gates:
        if g.left > g.right:
            new_gates.append(Gate(op=g.op, left=g.right, right=g.left, out=g.out))
        else:
            new_gates.append(g)
    sorted_gates = sorted(
        new_gates, key=lambda g: g.left if g.left[0] in ("x", "y", "z") else "zzz" + g.left
    )

    # Highest bit number - should be 44 with my data
    bit_num = max(int(w[1:]) for w in state.keys() if w[0] == "x")

    def find_gate(left: str, right: str, op: str) -> Gate:
        for g in sorted_gates:
            if (
                (g.left == left and g.right == right) or (g.right == left and g.left == right)
            ) and g.op == op:
                return g
        raise ValueError("Gate not found")

    # Output
    find_gate(left="x00", right="y00", op="XOR")
    # Carry
    last_carry = find_gate(left="x00", right="y00", op="AND").out

    for bn in range(1, bit_num + 1):
        bns = f"{bn:02}"

        try:
            # Find the intermediate sum, s_n
            print(f"s_n=x{bns} ^ y{bns} -> ", end="")
            s_n = find_gate(left="x" + bns, right="y" + bns, op="XOR").out
            print(s_n)

            # Find the output
            print(f"o_n={s_n} ^ {last_carry} -> ", end="")
            o_n = find_gate(left=s_n, right=last_carry, op="XOR").out
            print(o_n)
            if o_n != "z" + bns:
                print(f"/!\\ o_n={o_n}")

            print(f"a_n=x{bns} & y{bns} -> ", end="")
            a_n = find_gate(left="x" + bns, right="y" + bns, op="AND").out
            print(a_n)
            print(f"ac_n={s_n} & {last_carry} -> ", end="")
            ac_n = find_gate(left=s_n, right=last_carry, op="AND").out
            print(ac_n)
            print(f"c_n={a_n} | {ac_n} -> ", end="")
            c_n = find_gate(left=a_n, right=ac_n, op="OR").out
            print(c_n)

            print(
                f"{bns} ✅ last_carry={last_carry} intermediate_sum={s_n} output={o_n} ac_n={ac_n} carry={c_n}"
            )

            last_carry = c_n
        except Exception as e:
            print(f"/!\\ {str(e)}")
            raise

    # Manually fix the input for each bit until it completes
    """
    > ntr XOR gcc -> bfq
    > y39 AND x39 -> bng
    > jss AND mdg -> z18
    > y31 AND x31 -> z31
    > fqh XOR ctc -> hkh
    > mdg XOR jss -> hmt
    > x39 XOR y39 -> fjp
    > vgg OR pph -> z27
    """

    return -1

import re
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Optional, TextIO


@dataclass
class Device:
    a: int
    b: int = 0
    c: int = 0

    pointer: int = 0
    output: list[int] = field(default_factory=list)

    def get_combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
        raise ValueError(f"Invalid combo operand={operand}")

    def process_instruction(self, opcode: int, operand: int) -> None | int:
        combo = self.get_combo(operand)

        next_pointer = self.pointer + 2
        output = None

        match opcode:
            case 0:  # adv
                # this is the sneakiest thing here, binary division by 2**n is shifting a n bits to the right
                self.a //= 2**combo
            case 1:  # bxl
                self.b ^= operand
            case 2:  # bst
                self.b = combo % 8
            case 3:  # jnz
                if self.a != 0:
                    next_pointer = operand
            case 4:  # bxc
                self.b ^= self.c
            case 5:  # out
                output = combo % 8
            case 6:  # bdv
                self.b = self.a // 2**combo
            case 7:  # cdv
                self.c = self.a // 2**combo

        self.pointer = next_pointer
        return output

    def process_program(self, program: list[int], short_circuit: list[int] = None) -> bool:
        expected_it = iter(short_circuit or [])
        expected = next(expected_it, None)

        while self.pointer < len(program):
            output = self.process_instruction(program[self.pointer], program[self.pointer + 1])
            if output is not None:
                if short_circuit:
                    if output != expected:
                        return False
                    expected = next(expected_it, None)
                self.output.append(output)
        return True


def first(input: TextIO) -> str:
    device_s, instructions_s = input.read().split("\n\n")
    a, b, c = [int(n) for n in re.findall(r"\d+", device_s)]
    program = [int(n) for n in re.findall(r"\d+", instructions_s)]

    device = Device(a, b, c)
    device.process_program(program)

    return ",".join(str(n) for n in device.output)


def second(input: TextIO, desired: Optional[list[int]] = None) -> int:
    _, instructions_s = input.read().split("\n\n")
    program = [int(n) for n in re.findall(r"\d+", instructions_s)]

    if desired is None:
        desired = program

    # Current candidate, count of output numbers found
    candidates: Deque[tuple[int, int]] = deque([(0, 0)])
    solutions = []

    while candidates:
        c, num = candidates.popleft()
        c <<= 3

        future_candidates = []
        local_desired = desired[-num - 1 :]

        # 8 because it's a 3 bit computer, so we're always working 3 bits at a time
        # The first 3 bits of the number solve the last number of the output, then we add 3 bits at a time to find
        # the previous output number and so on, that's why local_desired is the end of desired.
        for a in range(8):
            number_to_test = c + a
            if Device(number_to_test).process_program(program, local_desired):
                if len(local_desired) == len(desired):
                    # This is finding all solutions, but because it's DFS, the first one found is the min
                    solutions.append(number_to_test)
                else:
                    future_candidates.append((number_to_test, num + 1))
        candidates.extendleft(reversed(future_candidates))

    return min(solutions)

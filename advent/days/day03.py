import re
from typing import TextIO


def first(input: TextIO) -> int:
    memory = input.read().strip()
    
    mul_groups = re.findall(r'mul\((\d+),(\d+)\)', memory)
    return sum(int(a)*int(b) for a, b in mul_groups)


def second(input: TextIO) -> int:
    memory = input.read().strip()
    matches = re.findall(r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)', memory)
    
    enabled = True
    total = 0
    for m in matches:
        if m.startswith('don'):
            enabled = False
        elif m.startswith('do'):
            enabled = True
        else:
            if not enabled:
                continue
            a, b = re.match(r'mul\((\d+),(\d+)\)', m).groups()
            total += int(a) * int(b)
    
    return total

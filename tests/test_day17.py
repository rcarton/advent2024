import io

from advent.days.day17 import first, second
from advent.utils import get_data_for_day

data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

data_2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


def test_first():
    assert first(io.StringIO(data)) == "4,6,3,5,6,3,5,2,1,0"


def test_second():
    assert second(get_data_for_day(17), [7, 1, 3, 4, 1, 2, 6, 7, 1]) == 46187030
    assert second(get_data_for_day(17)) == 109019476330651

import io

from advent.days.day03 import first, second

data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
data2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""


def test_first():
    assert first(io.StringIO(data)) == 161


def test_second():
    assert second(io.StringIO(data2)) == 48

import io

from advent.days.day21 import (
    first,
    second,
)
from advent.utils import get_data_for_day

data = """029A
980A
179A
456A
379A"""


def test_first():
    assert first(io.StringIO(data)) == 126384


def test_first__data():
    assert first(get_data_for_day(21)) == 171596


def test_second():
    assert second(io.StringIO(data)) == 154115708116294

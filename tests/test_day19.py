import io

from advent.days.day19 import first, second

data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def test_first():
    assert first(io.StringIO(data)) == 6


def test_second():
    assert second(io.StringIO(data)) == 16

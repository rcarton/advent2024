import io

from advent.days.day04 import first, second

data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def test_first():
    assert first(io.StringIO(data)) == 18


def test_second():
    assert second(io.StringIO(data)) == 9

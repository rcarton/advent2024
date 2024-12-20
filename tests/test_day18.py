import io

from advent.days.day18 import first, second

data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def test_first():
    assert first(io.StringIO(data), 7, 12) == 22


def test_second():
    assert second(io.StringIO(data), 7) == "6,1"

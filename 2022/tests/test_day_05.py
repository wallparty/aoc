from typing import Iterator

from aoc_2022.day_05 import part_1, part_2


def list_to_iter(t: list[str]) -> Iterator[str]:
    return (s for s in t)


def test_part_1() -> None:
    data = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    assert part_1(list_to_iter(data.splitlines())) == "CMZ"


def test_part_2() -> None:
    data = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    assert part_2(list_to_iter(data.splitlines())) == "MCD"

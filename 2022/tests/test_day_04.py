from aoc_2022.day_04 import part_2

part_2_input = {
    "2-4,6-8": 0,
    "2-3,4-5": 0,
    "5-7,7-9": 1,
    "2-8,3-7": 1,
    "6-6,4-6": 1,
    "2-6,4-8": 1,
    "6-8,2-4": 0,  # swapped input
    "4-5,2-3": 0,
    "7-9,5-7": 1,
    "3-7,2-8": 1,
    "4-6,6-6": 1,
    "4-8,2-6": 1,
}


def test_part_2() -> None:
    for k, v in part_2_input.items():
        assert v == part_2(iter((k,)))

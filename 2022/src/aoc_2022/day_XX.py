from itertools import tee
from typing import Iterator


def part_1(data: Iterator[str]) -> int:
    pass


def part_2(data: Iterator[str]) -> int:
    pass


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

from itertools import takewhile, tee
from operator import attrgetter
from typing import Iterator

from aoc_2022.iterutils import iter_len


class Elf:
    def __init__(self, carried_calories: Iterator[int]):
        self._carried_calories = list(carried_calories)
        self._total_calories = sum(self._carried_calories)

    @property
    def carried_calories(self) -> list[int]:
        return self._carried_calories

    @property
    def total_calories(self) -> int:
        return self._total_calories

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(carried_calories={self._carried_calories})"


def read_calories(lines: Iterator[str]) -> Iterator[Elf]:
    def not_blank(line: str) -> bool:
        return line != ""

    while True:
        result = map(int, takewhile(not_blank, lines))
        calories, calorie_len = iter_len(result)
        if calorie_len == 0:
            break
        yield Elf(calories)


def sort_calories(data: Iterator[str]) -> list[int]:
    return sorted(map(attrgetter("total_calories"), read_calories(data)), reverse=True)


def part_1(data: Iterator[str]) -> int:
    return sort_calories(data)[0]


def part_2(data: Iterator[str]) -> int:
    return sum(sort_calories(data)[:3])


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

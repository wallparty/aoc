from functools import reduce
from itertools import chain, tee
from string import ascii_letters
from typing import Iterator

from aoc_2022.iterutils import call_method, group_amounts, map_to_dict

ITEM_PRIORITY = {letter: score for score, letter in enumerate(ascii_letters, 1)}


class Rucksack:
    def __init__(self, contents: str):
        half = int(len(contents) / 2)
        first_half, second_half = contents[:half], contents[half:]
        self._first_half = list(first_half)
        self._second_half = list(second_half)

    def find_overlapping_items(self) -> set[str]:
        return set(self._first_half).intersection(self._second_half)

    @property
    def contents(self) -> list[str]:
        return self._first_half + self._second_half


class RucksackGroup:
    def __init__(self, rucksacks: Iterator[Rucksack]):
        self._rucksacks = rucksacks

    def find_id_badge(self) -> str:
        id_badges = reduce(
            set.intersection, map(lambda r: set(r.contents), self._rucksacks)
        )

        if len(id_badges) != 1:
            raise AttributeError("Expected one ID badge in a RucksackGroup")

        return "".join(id_badges)


def part_1(data: Iterator[str]) -> int:
    overlaps = map(call_method(Rucksack.find_overlapping_items), map(Rucksack, data))
    return sum(map_to_dict(ITEM_PRIORITY, chain.from_iterable(overlaps)))


def part_2(data: Iterator[str]) -> int:
    rucksack_groups = map(RucksackGroup, group_amounts(map(Rucksack, data), 3))
    return sum(
        map_to_dict(
            ITEM_PRIORITY,
            map(call_method(RucksackGroup.find_id_badge), rucksack_groups),
        )
    )


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

from itertools import starmap, tee
from typing import Iterator, NamedTuple


class Range(NamedTuple):
    min: int
    max: int


def parse_range(s: str) -> Range:
    r = Range(*tuple(map(int, s.split("-", maxsplit=2))))
    assert r.min <= r.max
    return r


def parse_ranges(line: str) -> tuple[Range, Range]:
    r1, r2 = tuple(map(parse_range, line.split(",", maxsplit=2)))
    return (r1, r2)


def are_ranges_coincident(r1: Range, r2: Range) -> bool:
    if (r1.max - r1.min) < (r2.max - r2.min):
        r1, r2 = r2, r1

    # Now r1 should be the largest range
    return r1.min <= r2.min and r1.max >= r2.max


def are_ranges_overlapping(r1: Range, r2: Range) -> bool:
    if r1.min > r2.min:
        r1, r2 = r2, r1

    # Now r1 should have the smallest min
    return r1.max >= r2.min


def part_1(data: Iterator[str]) -> int:
    return sum(starmap(are_ranges_coincident, map(parse_ranges, data)))


def part_2(data: Iterator[str]) -> int:
    return sum(starmap(are_ranges_overlapping, map(parse_ranges, data)))


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

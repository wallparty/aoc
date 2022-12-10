from itertools import chain, repeat, tee
from typing import Iterator

from aoc_2022.day_08 import Coord
from aoc_2022.iterutils import call_with, consume

DIRECTION_MAP = {
    "U": Coord(1, 0),
    "D": Coord(-1, 0),
    "L": Coord(0, -1),
    "R": Coord(0, 1),
}


class RopePhysics:
    def __init__(self, num_knots: int = 2) -> None:
        self.rope = list(map(call_with(0, 0), repeat(Coord, num_knots)))
        self.visited_spaces = {self.rope[-1]}

    def update(self, direction_name: str) -> None:
        self.rope[0] += DIRECTION_MAP[direction_name]
        for i in range(len(self.rope) - 1):
            self.rope[i + 1] = update_position(self.rope[i], self.rope[i + 1])
        self.visited_spaces.add(self.rope[-1])


def clamp(lower_bound: int, upper_bound: int, value: int) -> int:
    return max(min(value, upper_bound), lower_bound)


def unit_clamp(value: int) -> int:
    return clamp(-1, 1, value)


def update_position(knot1: Coord, knot2: Coord) -> Coord:
    separation = knot1 - knot2
    if abs(separation.row) > 1 or abs(separation.col) > 1:
        return knot2 + Coord(unit_clamp(separation.row), unit_clamp(separation.col))
    return knot2


def parse_line(line: str) -> Iterator[str]:
    direction, amount_str = line.split(" ", maxsplit=2)
    amount = int(amount_str)

    return repeat(direction, amount)


def run_simulation(rope: RopePhysics, data: Iterator[str]) -> None:
    consume(map(rope.update, chain.from_iterable(map(parse_line, data))))


def part_1(data: Iterator[str]) -> int:
    rope = RopePhysics()
    run_simulation(rope, data)
    return len(rope.visited_spaces)


def part_2(data: Iterator[str]) -> int:
    longer_rope = RopePhysics(10)
    run_simulation(longer_rope, data)
    return len(longer_rope.visited_spaces)


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

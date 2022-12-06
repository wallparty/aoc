import re
from itertools import chain, repeat, starmap, tee
from operator import itemgetter
from typing import Iterator

from aoc_2022.iterutils import call_method, call_with, consume, ingest_while, iter_len

CRATE_LINE_PATTERN = re.compile(r"(\[[A-Z]\]|\s{3,3})\s?")
CRATE_LETTER_PATTERN = re.compile(r"\[([A-Z])\]")
INSTRUCTION_PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")


class CrateStacks:
    def __init__(self) -> None:
        self._stacks: list[list[str]] = []

    def add_level(self, level: Iterator[str]) -> None:
        if self._stacks == []:
            level, level_len = iter_len(level)
            self._stacks = list(map(call_with(), repeat(list, level_len)))

        for stack_number, crate in enumerate(level):
            if crate == " ":
                continue

            self._stacks[stack_number].insert(0, crate)

    def move_crate(self, from_stack: int, to_stack: int) -> None:
        crate = self._stacks[from_stack - 1].pop()
        self._stacks[to_stack - 1].append(crate)

    def move_crates(self, amount: int, from_stack: int, to_stack: int) -> None:
        crates = list(
            map(call_with(self._stacks[from_stack - 1]), repeat(list.pop, amount))
        )
        self._stacks[to_stack - 1].extend(reversed(crates))

    def get_top_crates(self) -> str:
        return "".join(map(call_method(list.pop), self._stacks))

    def __str__(self) -> str:
        max_level = max(map(len, self._stacks))

        display = []
        for level in reversed(range(max_level)):
            line = []
            for stack in self._stacks:
                if level >= len(stack):
                    line.append("   ")
                else:
                    line.append(f"[{stack[level]}]")
            display.append(" ".join(line))

        display.append(" ".join(f" {i+1} " for i in range(len(self._stacks))))
        return "\n".join(display)


def parse_crates(line: str) -> Iterator[str]:
    return map(itemgetter(1), filter(None, CRATE_LINE_PATTERN.split(line)))


def parse_repeated_moves(line: str) -> Iterator[tuple[int, int]]:
    match = INSTRUCTION_PATTERN.fullmatch(line)
    if match is None:
        return iter(tuple())

    repeats, from_stack, to_stack = tuple(
        map(int, map(call_with(match), map(itemgetter, range(1, 4))))
    )

    return repeat((from_stack, to_stack), repeats)


def parse_blocked_moves(line: str) -> tuple[int, int, int]:
    match = INSTRUCTION_PATTERN.fullmatch(line)
    if match is None:
        return (0, 1, 1)

    amount, from_stack, to_stack = tuple(
        map(int, map(call_with(match), map(itemgetter, range(1, 4))))
    )

    return (amount, from_stack, to_stack)


def part_1(data: Iterator[str]) -> str:
    crate_stacks = CrateStacks()

    def stacks_are_being_added(line: str) -> bool:
        if "[" in line:
            crate_stacks.add_level(parse_crates(line))
            return True
        return False

    consume(
        chain(
            ingest_while(stacks_are_being_added, data),
            starmap(
                crate_stacks.move_crate,
                chain.from_iterable(map(parse_repeated_moves, data)),
            ),
        )
    )

    return crate_stacks.get_top_crates()


def part_2(data: Iterator[str]) -> str:
    crate_stacks = CrateStacks()

    def stacks_are_being_added(line: str) -> bool:
        if "[" in line:
            crate_stacks.add_level(parse_crates(line))
            return True
        return False

    consume(
        chain(
            ingest_while(stacks_are_being_added, data),
            starmap(
                crate_stacks.move_crates,
                map(parse_blocked_moves, data),
            ),
        )
    )

    return crate_stacks.get_top_crates()


def main(data: Iterator[str]) -> tuple[str, str]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

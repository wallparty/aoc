import re
from functools import partial, reduce
from itertools import repeat, takewhile, tee
from operator import add, attrgetter, mul, truth
from typing import Any, Callable, Iterator, NamedTuple, Optional, Type

from aoc_2022.iterutils import call_with, consume

OPERATIONS = {"+": add, "*": mul}


class InputMap(NamedTuple):
    regex: re.Pattern[str]
    reader: Callable[[str], Any]


def read_list(match: str) -> list[int]:
    return list(map(int, match.split(", ")))


def read_op(match: str) -> Callable[[int], int]:
    _, new_value = match.split(" = ", maxsplit=2)
    arg1, op_str, arg2 = new_value.split(" ", maxsplit=3)

    assert arg1 == "old"
    op: Callable[[int, int], int] = OPERATIONS[op_str]
    if arg2 == "old":
        operand = None
    else:
        operand = int(arg2)

    def op_fn(value: int) -> int:
        return op(value, operand if operand is not None else value)

    return op_fn


INPUT_MAPPINGS: dict[str, InputMap] = {
    "mid": InputMap(re.compile(r"Monkey (\d+):"), int),
    "item_worry_levels": InputMap(
        re.compile(r"\s+Starting items: ([\d, ]+)"), read_list
    ),
    "worry_level_op": InputMap(re.compile(r"\s+Operation: (.+)"), read_op),
    "modulo_value": InputMap(re.compile(r"\s+Test: divisible by (\d+)"), int),
    "throw_to_if_true": InputMap(re.compile(r"\s+If true: throw to monkey (\d+)"), int),
    "throw_to_if_false": InputMap(
        re.compile(r"\s+If false: throw to monkey (\d+)"), int
    ),
}


class Monkey:
    def __init__(self) -> None:
        self.mid = -1
        self.item_worry_levels: list[int] = []
        self.worry_level_op: Callable[[int], int] = lambda x: x
        self.modulo_value = -1
        self.throw_to_if_true = -1
        self.throw_to_if_false = -1
        self.items_inspected = 0

    @classmethod
    def parse(cls: Type["Monkey"], data: Iterator[str]) -> Optional["Monkey"]:
        monkey = cls()
        while (line := next(data, None)) is not None and line != "":
            for field, mapping in INPUT_MAPPINGS.items():
                if match := mapping.regex.match(line):
                    arg = match.group(1)
                    value = mapping.reader(arg)
                    setattr(monkey, field, value)

        if monkey.mid == -1:
            return None

        return monkey

    def inspect_item(self, item_worry_level: int) -> int:
        self.items_inspected += 1
        return self.worry_level_op(item_worry_level)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(mid={self.mid}, "
            f"item_worry_levels={self.item_worry_levels})"
        )


def read_monkeys(data: Iterator[str]) -> list[Monkey]:
    return list(
        filter(None, takewhile(truth, map(call_with(data), repeat(Monkey.parse))))
    )


def process_item_of(
    relieve: Callable[[int], int],
    monkey: Monkey,
    monkeys: list[Monkey],
    item_worry_level: int,
) -> None:
    post_inspect = monkey.inspect_item(item_worry_level)
    post_relief = relieve(post_inspect)
    if post_relief % monkey.modulo_value == 0:
        to_monkey = monkeys[monkey.throw_to_if_true]
    else:
        to_monkey = monkeys[monkey.throw_to_if_false]

    to_monkey.item_worry_levels.append(post_relief)


def take_turn(
    relieve: Callable[[int], int], monkey: Monkey, monkeys: list[Monkey]
) -> None:
    def inspect_first(items: list[int]) -> int:
        return items.pop(0)

    total_items_to_inspect = len(monkey.item_worry_levels)
    inspect_all = repeat(inspect_first, total_items_to_inspect)
    items_to_inspect = map(call_with(monkey.item_worry_levels), inspect_all)
    process_item = partial(process_item_of, relieve, monkey, monkeys)
    consume(map(process_item, items_to_inspect))


def compute_round(relieve: Callable[[int], int], monkeys: list[Monkey]) -> None:
    for monkey in monkeys:
        take_turn(relieve, monkey, monkeys)


def part_1(data: Iterator[str]) -> int:
    monkeys = read_monkeys(data)

    def relieve(level: int) -> int:
        return level // 3

    compute_round_part_1 = partial(compute_round, relieve)

    consume(map(call_with(monkeys), repeat(compute_round_part_1, 20)))
    most_inspected_monkeys = list(
        reversed(sorted(map(attrgetter("items_inspected"), monkeys)))
    )

    return reduce(mul, most_inspected_monkeys[:2], 1)


def part_2(data: Iterator[str]) -> int:
    monkeys = read_monkeys(data)
    total_modulo: int = reduce(mul, map(attrgetter("modulo_value"), monkeys))

    def relieve(level: int) -> int:
        return level % total_modulo

    compute_round_part_2 = partial(compute_round, relieve)

    consume(map(call_with(monkeys), repeat(compute_round_part_2, 10_000)))
    most_inspected_monkeys = list(
        reversed(sorted(map(attrgetter("items_inspected"), monkeys)))
    )

    return reduce(mul, most_inspected_monkeys[:2], 1)


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

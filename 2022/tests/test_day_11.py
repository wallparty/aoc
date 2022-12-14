from aoc_2022.day_11 import compute_round, read_monkeys, take_turn

INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


def relieve(level: int) -> int:
    return level // 3


def test_read_ops() -> None:
    monkeys = read_monkeys((i for i in INPUT.splitlines()))

    assert monkeys[0].worry_level_op(10) == 190
    assert monkeys[1].worry_level_op(10) == 16
    assert monkeys[2].worry_level_op(10) == 100
    assert monkeys[3].worry_level_op(10) == 13


def test_take_turn() -> None:
    monkeys = read_monkeys((i for i in INPUT.splitlines()))

    take_turn(relieve, monkeys[0], monkeys)

    assert monkeys[0].item_worry_levels == []
    assert monkeys[1].item_worry_levels == [54, 65, 75, 74]
    assert monkeys[2].item_worry_levels == [79, 60, 97]
    assert monkeys[3].item_worry_levels == [74, 500, 620]


def test_compute_round() -> None:
    monkeys = read_monkeys((i for i in INPUT.splitlines()))

    compute_round(relieve, monkeys)

    assert monkeys[0].item_worry_levels == [20, 23, 27, 26]
    assert monkeys[1].item_worry_levels == [2080, 25, 167, 207, 401, 1046]
    assert monkeys[2].item_worry_levels == []
    assert monkeys[3].item_worry_levels == []

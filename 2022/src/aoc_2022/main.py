import importlib
import shutil
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path
from string import Template
from typing import Any

from aoc_2022 import iterutils, utils

ROOT_DIR = Path(__file__).parent
TEST_DIR = ROOT_DIR.parent.parent.joinpath("tests")


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Manage AoC solutions",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    action_parsers = parser.add_subparsers(dest="action", help="the action to take")

    run_parser = action_parsers.add_parser(
        "run",
        description="Run AoC solutions",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    run_parser.add_argument(
        "day", nargs="?", default=None, type=int, help="the day to run"
    )

    generate_parser = action_parsers.add_parser(
        "generate",
        description="Generate AoC solution boilerplate",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    generate_parser.add_argument(
        "day", type=int, help="the day to generate boilerplate code for"
    )

    return parser


def get_display(result: Any) -> str:
    if isinstance(result, int):
        return f"{result: 8}"
    elif isinstance(result, str):
        if len(result) > 10:
            return "\n" + result
        return result
    else:
        return str(result)


def run_one(puzzle_id: int) -> None:
    module_name = f"aoc_2022.day_{puzzle_id:02}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return

    if "main" not in dir(module):
        raise AttributeError(f"{module_name} must have a main method")

    data = utils.fetch_input(puzzle_id)

    a, b = module.main(data)
    print(f"{puzzle_id:02} -> {get_display(a)}, {get_display(b)}")


def run_all() -> None:
    iterutils.consume(map(run_one, range(1, 26)))


def run(puzzle_id: int | None) -> None:
    if puzzle_id is None:
        run_all()
    else:
        run_one(puzzle_id)


def generate(puzzle_id: int) -> None:
    solution_template = ROOT_DIR.joinpath("day_XX.py")
    new_solution = solution_template.with_stem(f"day_{puzzle_id:02}")
    if new_solution.exists():
        print(new_solution, "already exists, skipping...")
    else:
        shutil.copyfile(solution_template, new_solution)

    test_template = TEST_DIR / "data" / "day_XX.toml.fmt"
    new_test = test_template.with_name(f"day_{puzzle_id:02}.toml")
    if new_test.exists():
        print(new_test, "already exists, skipping...")
    else:
        with test_template.open(mode="r", encoding="utf-8") as f:
            template = Template(f.read())

        with new_test.open(mode="w", encoding="utf-8") as f:
            content = template.substitute(
                {"part_1_output": 0, "part_2_output": 0, "input": ""}
            )
            f.write(content)


def main() -> int:
    args = make_parser().parse_args()

    action, action_args = {
        "run": (run, (args.day,)),
        "generate": (generate, (args.day,)),
    }.get(args.action, (lambda: None, tuple()))

    action(*action_args)
    return 0


if __name__ == "__main__":
    exit(main())

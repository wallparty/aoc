import importlib
from itertools import cycle
from pathlib import Path
import tomllib
from typing import Any, Callable, Iterator, cast

ProblemInput = Iterator[str]
ProblemOutput = int | str
PartFn = Callable[[ProblemInput], ProblemOutput]
Data = tuple[str, tuple[ProblemInput, ProblemOutput]]

ROOT = Path(__file__).parent

__all__ = [
    "Data",
    "IdProvider",
    "PartFn",
    "ProblemInput",
    "ProblemOutput",
    "generate_parameters",
    "get_part_fn",
]


class IdProvider:
    def __init__(self) -> None:
        """Create an object that will build test IDs argument-by-argument."""
        self._formats: Iterator[Callable[[Any], str]] = cycle(
            [lambda x: f"day_{x:02}", lambda x: f"part_{x}", lambda x: str(x[0])]
        )

    def __call__(self, arg: Any) -> str:
        """Call the next formatting function on the next test argument."""
        return next(self._formats)(arg)


def get_part_fn(puzzle_id: int, part_number: int) -> PartFn:
    """Return the function that runs part 1 or 2 of the puzzle's solution.

    Args
    ----
        puzzle_id (int): the puzzle ID (day number).
        part_number (int): the part number.

    Raises
    ------
        ImportError: if the puzzle solution doesn't exist yet.
        AttributeError: if the part of the solution doesn't exist yet.

    Returns
    -------
        PartFn: the function that runs a part of the solution.
    """
    module_name = f"aoc_2022.day_{puzzle_id:02}"
    module = importlib.import_module(module_name)
    return cast(PartFn, module.__getattribute__(f"part_{part_number}"))


def generate_parameters() -> Iterator[tuple[int, int, Data]]:
    """Generate tuples used as test parameters.

    Yields
    ------
        Iterator[tuple[int, int, Data]]: the test function parameters.
    """
    for puzzle_id in range(1, 26):
        for part_number in (1, 2):
            if not _has_written_solution(puzzle_id, part_number):
                continue

            all_test_data = _read_test_data(puzzle_id, part_number)
            if all_test_data is None:
                continue

            yield from ((puzzle_id, part_number, data) for data in all_test_data)


def _read_test_data(puzzle_id: int, part_number: int) -> Iterator[Data] | None:
    test_data_file = ROOT / "data" / f"day_{puzzle_id:02}.toml"
    part_key = f"part_{part_number}"

    try:
        with test_data_file.open(mode="rb") as f:
            raw = tomllib.load(f)
            for name, test_data in raw[part_key].items():
                test_input = (d for d in test_data["input"].splitlines())
                test_output = test_data["output"]
                yield (name, (test_input, test_output))

    except (IOError, KeyError):
        pass

    return None


def _has_written_solution(puzzle_id: int, part_number: int) -> bool:
    try:
        get_part_fn(puzzle_id, part_number)
    except (ModuleNotFoundError, AttributeError):
        return False

    return True

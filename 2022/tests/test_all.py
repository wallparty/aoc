from typing import Callable, Iterator, Any, cast
import importlib

import pytest

ProblemInput = Iterator[str]
ProblemOutput = int | str
PartFn = Callable[[ProblemInput], ProblemOutput]
Data = tuple[str, tuple[ProblemInput, ProblemOutput]]


class IdProvider:
    def __init__(self) -> None:
        self._day_id: str | None = None

    def __call__(self, arg: Any) -> str:
        if isinstance(arg, int):
            if self._day_id is None:
                self._day_id = f"day_{arg:02}"
                return self._day_id
            else:
                self._day_id = None
                return f"part_{arg:02}"
        elif isinstance(arg, tuple):
            return str(arg[0])

        return ""


def generate_parameters() -> Iterator[tuple[int, int, Data]]:
    for puzzle_id in range(1, 26):
        for part_number in (1, 2):
            if not is_valid(puzzle_id, part_number):
                continue

            yield (puzzle_id, part_number, ("success", (("a" for _ in range(10)), 2)))


def get_part_fn(puzzle_id: int, part_number: int) -> PartFn:
    module_name = f"aoc_2022.day_{puzzle_id:02}"
    module = importlib.import_module(module_name)
    return cast(PartFn, module.__getattribute__(f"part_{part_number}"))


def is_valid(puzzle_id: int, part_number: int) -> bool:
    module_name = f"aoc_2022.day_{puzzle_id:02}"
    try:
        module = importlib.import_module(module_name)
        module.__getattribute__(f"part_{part_number}")
    except (ModuleNotFoundError, AttributeError):
        return False

    return True


@pytest.mark.skip("Not ready yet")
@pytest.mark.parametrize(
    "puzzle_id,part_number,data", generate_parameters(), ids=IdProvider()
)
def test_part(puzzle_id: int, part_number: int, data: Data) -> None:
    part_fn = get_part_fn(puzzle_id, part_number)
    part_data, output = data[1]
    assert part_fn(part_data) == output

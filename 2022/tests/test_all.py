import pytest

from .utils import Data, IdProvider, generate_parameters, get_part_fn


@pytest.mark.parametrize(
    "puzzle_id,part_number,data", generate_parameters(), ids=IdProvider()
)
def test_part(puzzle_id: int, part_number: int, data: Data) -> None:
    part_fn = get_part_fn(puzzle_id, part_number)
    part_data, output = data[1]
    assert part_fn(part_data) == output

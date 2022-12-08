from itertools import accumulate

import pytest

from aoc_2022.day_08 import (
    Coord,
    count_visible,
    generate_visible_tree_lines,
    get_score_at,
    observe_row_visibility,
    observe_visibility,
)

VISIBILITY_INPUT = {
    "00000": [0],
    "00100": [0, 2],
    "00111": [0, 2],
    "00101": [0, 2],
    "00102": [0, 2, 4],
    "04102": [0, 1],
    "23459": [0, 1, 2, 3, 4],
}

ROW_INPUT: dict[tuple[int, str], list[tuple[int, int]]] = {
    (0, "00000"): [(0, 0), (0, 4)],
    (1, "00100"): [(1, 0), (1, 2), (1, 4), (1, 2)],
}

VISIBLE_INPUT = {
    (2, (0, 1, 1, 5)): 4,
    (2, (0, 4, 2, 1)): 2,
    (0, (5, 1, 0, 0)): 1,
    (5, (1, 1, 1, 1)): 4,
    (2, tuple()): 0,
}

GRID = [
    [0, 1, 1, 0],
    [0, 2, 2, 0],
    [0, 2, 3, 1],
    [0, 1, 1, 0],
]

COORD_INPUT = {
    Coord(0, 0): [[0, 0, 0], [1, 1, 0]],
    Coord(2, 2): [[1], [2, 1], [1], [2, 0]],
    Coord(2, 1): [[1], [2, 1], [3, 1], [0]],
}

SCORE_INPUT = {
    Coord(0, 0): 0,
    Coord(2, 2): 4,
    Coord(1, 2): 1,
}


@pytest.mark.parametrize(
    "line,expected", VISIBILITY_INPUT.items(), ids=VISIBILITY_INPUT
)
def test_observe_visibility(line: str, expected: list[int]) -> None:
    calculated = list(observe_visibility(line))
    assert calculated == expected


@pytest.mark.parametrize(
    "row,expected", ROW_INPUT.items(), ids=map(lambda x: f"{x[0]} -> {x[1]}", ROW_INPUT)
)
def test_observe_row_visibility(
    row: tuple[int, str], expected: list[tuple[int, int]]
) -> None:
    calculated_iter, used_row = observe_row_visibility(*row)
    calculated = list(calculated_iter)

    assert calculated == expected
    assert used_row == row[1]


def test_accumulate() -> None:
    t = [0, 0, 1, 3, 1, 2, 4]

    assert list(accumulate(t, max)) == [0, 0, 1, 3, 3, 3, 4]


def test_zip() -> None:
    rows = ["abcde", "fghij", "klmno", "pqrst", "uvwxy"]
    rows_iter = (row for row in rows)
    cols = list(map("".join, zip(*rows_iter)))
    assert cols[0] == "afkpu"


def test_multi_zip() -> None:
    rows = ["abcde", "fghij", "klmno", "pqrst", "uvwxy"]
    rows_iter = (row for row in rows)

    def get_results(c: str) -> tuple[str, int]:
        return c, 0

    thing_iter, results_iter = zip(*map(get_results, rows_iter))

    cols = list(map("".join, zip(*thing_iter)))
    results = list(results_iter)

    assert cols[0] == "afkpu"
    assert results == [0, 0, 0, 0, 0]


@pytest.mark.parametrize("data,expected", VISIBLE_INPUT.items())
def test_count_visible(data: tuple[int, tuple[int]], expected: int) -> None:
    current_height, trees = data

    assert expected == count_visible(current_height, (t for t in trees))


@pytest.mark.parametrize(
    "coord,expected", COORD_INPUT.items(), ids=map(str, COORD_INPUT)
)
def test_generate_visible_tree_lines(coord: Coord, expected: list[list[int]]) -> None:
    lines = list(filter(None, map(list, generate_visible_tree_lines(GRID, coord))))

    assert expected == lines


@pytest.mark.parametrize(
    "coord,expected", SCORE_INPUT.items(), ids=map(str, SCORE_INPUT)
)
def test_get_score_at(coord: Coord, expected: list[list[int]]) -> None:
    assert expected == get_score_at(GRID, coord)

from dataclasses import dataclass
from functools import partial, reduce
from itertools import (
    accumulate,
    chain,
    compress,
    count,
    pairwise,
    product,
    repeat,
    starmap,
    takewhile,
    tee,
)
from operator import add, gt, mul, ne, sub
from typing import Iterator

from aoc_2022.iterutils import iter_len, transpose


@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    def __add__(self, o: object) -> "Coord":
        if not isinstance(o, Coord):
            raise ValueError("Cannot add non-coordinate to coordinate object")
        return Coord(self.row + o.row, self.col + o.col)

    def __sub__(self, o: object) -> "Coord":
        if not isinstance(o, Coord):
            raise ValueError("Cannot subtract non-coordinate from coordinate object")
        return Coord(self.row - o.row, self.col - o.col)

    def __mul__(self, o: object) -> "Coord":
        if not isinstance(o, int):
            raise ValueError("Only scalar multiplication is supported")
        return Coord(self.row * o, self.col * o)

    def __rmul__(self, o: object) -> "Coord":
        return self * o

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Coord):
            return False
        return (self.row, self.col) == (o.row, o.col)

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __hash__(self) -> int:
        return hash((self.row, self.col))


def observe_visibility(tree_line: str) -> Iterator[int]:
    cumulative_max_height = accumulate(map(int, tree_line), max)
    where_tree_height_changes = starmap(ne, pairwise(cumulative_max_height))
    # Because we are calculating where tree height changes, we need to start at the
    # next index along
    next_indices = count(1)
    # We also miss out on the first index 0 which is always visible, so add it
    return chain((0,), compress(next_indices, where_tree_height_changes))


def observe_visibility_in_reverse(tree_line: str) -> Iterator[int]:
    max_index = len(tree_line) - 1
    return map(partial(sub, max_index), observe_visibility(tree_line[::-1]))


def observe_row_visibility(
    row_number: int, tree_row: str
) -> tuple[Iterator[tuple[int, int]], str]:
    trees_visible_in_row = chain(
        observe_visibility(tree_row), observe_visibility_in_reverse(tree_row)
    )
    visible_coords = zip(repeat(row_number), trees_visible_in_row)
    return visible_coords, tree_row


def observe_column_visibility(
    column_number: int, tree_column: str
) -> Iterator[tuple[int, int]]:
    trees_visible_in_column = chain(
        observe_visibility(tree_column), observe_visibility_in_reverse(tree_column)
    )
    visible_coords = zip(trees_visible_in_column, repeat(column_number))
    return visible_coords


def count_visible(current_height: int, tree_line: Iterator[int]) -> int:
    """Count the number of visible trees along a tree line."""
    tree_is_visible = partial(gt, current_height)
    tree_line, tree_line_len = iter_len(tree_line)
    if tree_line_len == 0:
        return 0
    total_visible_trees = sum(1 for _ in takewhile(tree_is_visible, tree_line))

    if total_visible_trees < tree_line_len:
        # If we didn't reach the end of the line, we have to add one as we can see
        # the tree we're being blocked by
        return total_visible_trees + 1

    return total_visible_trees


def get_at_grid(tree_grid: list[list[int]], coord: Coord) -> int:
    return tree_grid[coord.row][coord.col]


def get_score_at(tree_grid: list[list[int]], coord: Coord) -> int:
    """Get the score of a coordinate location in the tree grid."""
    current_height = get_at_grid(tree_grid, coord)
    line_visibility = partial(count_visible, current_height)
    scenic_scores = map(line_visibility, generate_visible_tree_lines(tree_grid, coord))
    scenic_score = reduce(mul, scenic_scores, 1)
    return scenic_score


def generate_visible_tree_lines(
    tree_grid: list[list[int]], coord: Coord
) -> Iterator[Iterator[int]]:
    """Generate all four visible lines from a coordinate in the tree grid."""
    grid_size = len(tree_grid)
    directions = [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1)]

    height_at = partial(get_at_grid, tree_grid)
    see_along = partial(add, coord)

    def is_bound(coord: Coord) -> bool:
        return 0 <= coord.row < grid_size and 0 <= coord.col < grid_size

    def seen_line(along: Coord) -> Iterator[Coord]:
        line = map(partial(mul, along), count(1))
        return takewhile(is_bound, map(see_along, line))

    return (map(height_at, seen_line(d)) for d in directions)


def part_1(data: Iterator[str]) -> int:
    row_visibilities_iter, piped_data = transpose(
        starmap(observe_row_visibility, enumerate(data))
    )
    columns = map("".join, transpose(piped_data))

    row_visibilities = chain.from_iterable(row_visibilities_iter)
    column_visibilities = chain.from_iterable(
        starmap(observe_column_visibility, enumerate(columns))
    )

    all_visible_trees = set(chain(row_visibilities, column_visibilities))

    return len(all_visible_trees)


def part_2(data: Iterator[str]) -> int:
    def read_row(row: str) -> list[int]:
        return list(map(int, row))

    tree_grid = list(map(read_row, data))
    grid_size = len(tree_grid)
    get_scores_from = partial(get_score_at, tree_grid)
    all_coords = starmap(Coord, product(range(grid_size), repeat=2))

    return max(map(get_scores_from, all_coords))


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

from itertools import tee, product, starmap
from functools import partial
from typing import Iterator, TypeVar, Callable
from string import ascii_lowercase
from collections import defaultdict
from dataclasses import dataclass, field
from queue import PriorityQueue

from aoc_2022.iterutils import map_to_dict

START_HEIGHT = -1
END_HEIGHT = len(ascii_lowercase)
T = TypeVar("T")


class Node:
    def __init__(self, row: int, col: int, height: int):
        self.row = row
        self.col = col
        self.height = height
        self.neighbours: set["Node"] = set()

    def distance_to(self, other: "Node") -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return (
            self.row == other.row
            and self.col == other.col
            and self.height == other.height
        )

    def __hash__(self) -> int:
        return hash((self.row, self.col, self.height))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.row}, {self.col}, {self.height}, "
            f"neighbours=<set len={len(self.neighbours)}>)"
        )


@dataclass(order=True)
class PrioritisedNode:
    f_scores: int
    node: Node = field(compare=False)


def read_heightmap(data: Iterator[str]) -> list[list[int]]:
    height_map = dict(zip(ascii_lowercase, range(len(ascii_lowercase))))
    height_map["S"] = START_HEIGHT
    height_map["E"] = END_HEIGHT

    def read_line(line: str) -> list[int]:
        return list(map_to_dict(height_map, iter(line)))

    return list(map(read_line, data))


def get_2d_point(field: list[list[T]], row: int, col: int) -> T:
    return field[row][col]


def create_nodes(heightmap: list[list[int]]) -> list[Node]:
    def traversible(this_node: Node, next_node: Node) -> bool:
        return next_node.height - this_node.height <= 1

    max_rows = len(heightmap)
    max_cols = len(heightmap[0])
    height_at = partial(get_2d_point, heightmap)

    def get_neighbours(row: int, col: int) -> Iterator[tuple[int, int]]:
        if row - 1 >= 0:
            yield (row - 1, col)
        if row + 1 < max_rows:
            yield (row + 1, col)
        if col - 1 >= 0:
            yield (row, col - 1)
        if col + 1 < max_cols:
            yield (row, col + 1)

    # Create nodes
    coords = list(product(range(max_rows), range(max_cols)))
    heights = starmap(height_at, coords)
    coords_and_heights = zip(*zip(*coords), heights)
    flat_nodes = starmap(Node, coords_and_heights)
    nodes = dict(zip(coords, flat_nodes))

    # Then link them
    for coord, node in nodes.items():
        neighbouring_nodes = map_to_dict(nodes, get_neighbours(*coord))
        traversible_from = partial(traversible, node)
        node.neighbours = set(filter(traversible_from, neighbouring_nodes))

    return list(nodes.values())


def find_start_and_end(nodes: list[Node]) -> tuple[Node, Node]:
    start_node = end_node = None

    for node in nodes:
        if node.height == START_HEIGHT:
            node.height = START_HEIGHT + 1
            start_node = node
        elif node.height == END_HEIGHT:
            node.height = END_HEIGHT - 1
            end_node = node

    assert start_node is not None, "couldn't find start node"
    assert end_node is not None, "couldn't find end node"

    return (start_node, end_node)


def recreate_path(came_from: dict[Node, Node], current: Node) -> list[Node]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path


def A_star(start: Node, end: Node, h: Callable[[Node], int]) -> list[Node]:
    known: PriorityQueue[PrioritisedNode] = PriorityQueue()
    known_set = set()
    came_from: dict[Node, Node] = {}

    g_scores: defaultdict[Node, int] = defaultdict(lambda: 1_000_000_000)
    g_scores[start] = 0

    f_scores: defaultdict[Node, int] = defaultdict(lambda: 1_000_000_000)
    f_scores[start] = h(start)

    known.put(PrioritisedNode(g_scores[start], start))
    known_set.add(start)

    while not known.empty():
        current = known.get().node
        if current == end:
            return recreate_path(came_from, current)

        known_set.remove(current)

        for neighbour in current.neighbours:
            tentative_g_score = g_scores[current] + 1
            if tentative_g_score < g_scores[neighbour]:
                came_from[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_scores[neighbour] = tentative_g_score + h(neighbour)
                if neighbour not in known_set:
                    known.put(PrioritisedNode(f_scores[neighbour], neighbour))
                    known_set.add(neighbour)

    return []


def part_1(data: Iterator[str]) -> int:
    heightmap = read_heightmap(data)
    nodes = create_nodes(heightmap)
    start_node, end_node = find_start_and_end(nodes)
    heuristic = end_node.distance_to

    path = A_star(start_node, end_node, heuristic)
    return len(path) - 1


def part_2(data: Iterator[str]) -> int:
    heightmap = read_heightmap(data)
    nodes = create_nodes(heightmap)
    _, end_node = find_start_and_end(nodes)
    start_nodes = filter(lambda x: x.height == 0, nodes)

    possible_paths = filter(
        None, map(lambda x: A_star(x, end_node, end_node.distance_to), start_nodes)
    )
    return min(map(len, possible_paths)) - 1


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

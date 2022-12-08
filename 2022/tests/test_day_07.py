from aoc_2022.day_07 import Ingestor
from aoc_2022.iterutils import consume


def test_get_children_recursively_one_level() -> None:
    data = ["$ cd /", "$ ls", "dir a", "dir b", "dir c", "$ cd a", "$ ls", "10 d"]
    ingestor = Ingestor()

    consume(map(ingestor, data))

    dirs = list(ingestor._root.get_children_recursively())

    assert len(dirs) == 4


def test_get_children_recursively_two_levels() -> None:
    data = ["$ cd /", "$ ls", "dir a", "$ cd a", "$ ls", "dir b", "dir c", "10 d"]
    ingestor = Ingestor()

    consume(map(ingestor, data))

    dirs = list(ingestor._root.get_children_recursively())

    assert len(dirs) == 4

import enum
from functools import partial
from itertools import tee
from operator import attrgetter, gt, itemgetter, lt
from typing import Iterator, Optional

from aoc_2022.iterutils import consume


class Directory:
    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        self.name = name
        self.parent = parent
        self._children: dict[str, Directory] = {}
        self._files: list[tuple[str, int]] = []

    def add_directory(self, directory: "Directory") -> None:
        self._children[directory.name] = directory

    def get_directory(self, dir_name: str) -> "Directory":
        return self._children[dir_name]

    def add_file(self, file_name: str, file_size: int) -> None:
        self._files.append((file_name, file_size))

    def get_children_recursively(self) -> Iterator["Directory"]:
        def recurse(d: "Directory") -> Iterator["Directory"]:
            yield d
            for child in d._children.values():
                yield from recurse(child)

        return recurse(self)

    @property
    def total_size(self) -> int:
        return sum(map(itemgetter(1), self._files))

    @property
    def total_recursive_size(self) -> int:
        return sum(map(attrgetter("total_size"), self.get_children_recursively()))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r})"


class IngestMode(enum.Enum):
    COMMAND = enum.auto()
    LIST_OUTPUT = enum.auto()


class Ingestor:
    _root: Directory
    _cwd: Directory

    def __init__(self) -> None:
        self._has_root = False
        self._mode = IngestMode.COMMAND

    def __call__(self, line: str) -> None:
        if is_command(line):
            self._mode = IngestMode.COMMAND
            self.handle_command(line)

        elif is_output(line) or self._mode == IngestMode.LIST_OUTPUT:
            self.handle_list_output(line)

    def handle_command(self, prompt: str) -> None:
        command, args = parse_command(prompt)

        if command == "cd":
            location = args[0]
            if location == "..":
                if self._cwd.parent is None:
                    raise ValueError("cannot navigate past root")
                self._cwd = self._cwd.parent
            else:
                if not self._has_root:
                    self._has_root = True
                    self._root = Directory(location)
                    self._cwd = self._root
                else:
                    self._cwd = self._cwd.get_directory(location)

        elif command == "ls":
            self._mode = IngestMode.LIST_OUTPUT

    def handle_list_output(self, output: str) -> None:
        fid, name = output.split(" ", maxsplit=2)

        if fid == "dir":
            new_dir = Directory(name, self._cwd)
            self._cwd.add_directory(new_dir)
        elif fid.isnumeric():
            size = int(fid)
            self._cwd.add_file(name, size)

    @property
    def directories(self) -> Iterator[Directory]:
        return self._root.get_children_recursively()


def is_command(line: str) -> bool:
    return line.startswith("$")


def is_output(line: str) -> bool:
    return not is_command(line)


def parse_command(line: str) -> tuple[str, list[str]]:
    split = line.split()
    return (split[1], split[2:])


def part_1(data: Iterator[str]) -> int:
    size_limit = 100_000  # dir_size <= 100_000

    ingestor = Ingestor()

    consume(map(ingestor, data))

    return sum(
        filter(
            partial(gt, size_limit),
            map(attrgetter("total_recursive_size"), ingestor.directories),
        )
    )


def part_2(data: Iterator[str]) -> int:
    total_free_space = 70_000_000
    required_available_space = 30_000_000

    ingestor = Ingestor()

    consume(map(ingestor, data))

    total_used_space = ingestor._root.total_recursive_size
    total_available_space = total_free_space - total_used_space

    space_to_free = required_available_space - total_available_space

    return int(
        min(
            filter(
                partial(lt, space_to_free),
                map(attrgetter("total_recursive_size"), ingestor.directories),
            )
        )
    )


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

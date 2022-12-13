from aoc_2022.day_12 import read_heightmap


def test_read_heightmap() -> None:
    data = ["Sabc", "gfed", "hijk", "Enml"]
    heightmap = read_heightmap((d for d in data))

    assert heightmap == [
        [-1, 0, 1, 2],
        [6, 5, 4, 3],
        [7, 8, 9, 10],
        [26, 13, 12, 11],
    ]

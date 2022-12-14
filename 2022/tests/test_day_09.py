from aoc_2022.day_09 import Coord, RopePhysics, run_simulation


def test_long_movements() -> None:
    data = ["R 5", "U 8"]
    rope = RopePhysics(10)
    run_simulation(rope, (d for d in data))

    assert len(rope.visited_spaces) == 1
    assert rope.rope == [
        Coord(8, 5),
        Coord(7, 5),
        Coord(6, 5),
        Coord(5, 5),
        Coord(4, 5),
        Coord(4, 4),
        Coord(3, 3),
        Coord(2, 2),
        Coord(1, 1),
        Coord(0, 0),
    ]

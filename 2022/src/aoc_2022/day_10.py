from functools import partial
from itertools import accumulate, chain, islice, pairwise, repeat, starmap, tee
from operator import mul
from typing import Callable, Iterator

from aoc_2022.iterutils import call_with

Instruction = Callable[[int], int]


def rsub(b: int, a: int) -> int:
    return a - b


def rmod(b: int, a: int) -> int:
    return a % b


def process(instruction: str) -> Iterator[int]:
    strip = instruction.split(" ", maxsplit=2)
    command, args = strip[0], strip[1:]

    if command == "noop":
        return iter((0,))
    elif command == "addx":
        to_add = int(args[0])
        return iter((0, to_add))
    else:
        print("oh fiddlesticks!!")
        return iter((0,))


def ingest(values: Iterator[int], tick_amount: int) -> int:
    return sum(islice(values, tick_amount))


def in_range(range_size: int, lower_bound: int, point: int) -> bool:
    upper_bound = lower_bound + range_size
    return lower_bound <= point < upper_bound


def draw_pixel_if_lit(is_lit: bool) -> str:
    return "#" if is_lit else "."


def part_1(data: Iterator[str]) -> int:
    ticks = [0, 20, 60, 100, 140, 180, 220]
    tick_amounts = starmap(rsub, pairwise(ticks))
    initial_value = 1

    processed_values = chain((initial_value,), chain.from_iterable(map(process, data)))

    get_next_tick = partial(ingest, processed_values)
    total_values = accumulate(map(get_next_tick, tick_amounts))
    at_tick = ticks[1:]
    signal_strengths = starmap(mul, zip(total_values, at_tick))

    return sum(signal_strengths)


def part_2(data: Iterator[str]) -> str:
    sprite_size = 3

    screen_width = 40
    screen_height = 6
    screen_wrapper = partial(rmod, screen_width)
    crt_head_positions = map(screen_wrapper, range(screen_width * screen_height))

    # As the CRT is starting from zero, we no longer need to set the intial value of our
    # processed values to 1! We still need to initialise it though, haha (oops)
    processed_values = chain((0,), chain.from_iterable(map(process, data)))

    sprite_locations = accumulate(processed_values)
    on_sprite = partial(in_range, sprite_size)

    is_lit_pixel = starmap(on_sprite, zip(sprite_locations, crt_head_positions))

    pixels = map(draw_pixel_if_lit, is_lit_pixel)
    slice_row = partial(lambda x: islice(x, screen_width))
    screen = map("".join, map(call_with(pixels), repeat(slice_row, screen_height)))

    return "\n".join(screen)


def main(data: Iterator[str]) -> tuple[int, str]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

from itertools import starmap, tee, takewhile
from operator import itemgetter, gt
from functools import partial
from typing import Iterator

from .iterutils import call_with


def ngram(s: str, n: int) -> Iterator[str]:
    limits = zip(range(0, len(s)), range(n, len(s)))
    slices = starmap(slice, limits)
    slice_getters = map(itemgetter, slices)

    return map(call_with(s), slice_getters)


def detect_marker(signal: str, marker_size: int) -> int:
    marker_candidates = ngram(signal, marker_size)
    incorrect_marker_length = partial(gt, marker_size)
    marker_lengths = map(len, (map(lambda x: set(x), marker_candidates)))
    used_candidates = takewhile(incorrect_marker_length, marker_lengths)

    return marker_size + sum(1 for _ in used_candidates)


def detect_start_of_packet_marker(signal: str) -> int:
    return detect_marker(signal, 4)


def detect_start_of_message_marker(signal: str) -> int:
    return detect_marker(signal, 14)


def part_1(data: Iterator[str]) -> int:
    return detect_start_of_packet_marker(next(data))


def part_2(data: Iterator[str]) -> int:
    return detect_start_of_message_marker(next(data))


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

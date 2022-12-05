from enum import Enum
from itertools import tee
from typing import Iterator

RpsMove = Enum("RpsMove", "ROCK PAPER SCISSORS NONE")
RpsOutcome = Enum("RpsOutcome", "WIN DRAW LOSS")

INPUTS = {"A": RpsMove.ROCK, "B": RpsMove.PAPER, "C": RpsMove.SCISSORS}
OUTPUTS = {"X": RpsMove.ROCK, "Y": RpsMove.PAPER, "Z": RpsMove.SCISSORS}
OUTCOMES = {"X": RpsOutcome.LOSS, "Y": RpsOutcome.DRAW, "Z": RpsOutcome.WIN}


def resolve(opponent: RpsMove, response: RpsMove) -> RpsOutcome:
    if (
        (opponent == RpsMove.ROCK and response == RpsMove.SCISSORS)
        or (opponent == RpsMove.PAPER and response == RpsMove.ROCK)
        or (opponent == RpsMove.SCISSORS and response == RpsMove.PAPER)
    ):
        return RpsOutcome.LOSS

    if (
        (response == RpsMove.ROCK and opponent == RpsMove.SCISSORS)
        or (response == RpsMove.PAPER and opponent == RpsMove.ROCK)
        or (response == RpsMove.SCISSORS and opponent == RpsMove.PAPER)
    ):
        return RpsOutcome.WIN

    return RpsOutcome.DRAW


def decide(opponent: RpsMove, outcome: RpsOutcome) -> RpsMove:
    if outcome == RpsOutcome.DRAW:
        return opponent

    if outcome == RpsOutcome.LOSS:
        if opponent == RpsMove.ROCK:
            return RpsMove.SCISSORS
        elif opponent == RpsMove.PAPER:
            return RpsMove.ROCK
        elif opponent == RpsMove.SCISSORS:
            return RpsMove.PAPER

    if outcome == RpsOutcome.WIN:
        if opponent == RpsMove.ROCK:
            return RpsMove.PAPER
        elif opponent == RpsMove.PAPER:
            return RpsMove.SCISSORS
        elif opponent == RpsMove.SCISSORS:
            return RpsMove.ROCK

    return RpsMove.NONE


def score(move: RpsMove, outcome: RpsOutcome) -> int:
    return {RpsMove.ROCK: 1, RpsMove.PAPER: 2, RpsMove.SCISSORS: 3}.get(move, 0) + {
        RpsOutcome.LOSS: 0,
        RpsOutcome.DRAW: 3,
        RpsOutcome.WIN: 6,
    }.get(outcome, 0)


def score_round_part_1(round: str) -> int:
    opponent_code, response_code = round.split(" ", maxsplit=2)
    opponent = INPUTS[opponent_code]
    response = OUTPUTS[response_code]
    outcome = resolve(opponent, response)
    return score(response, outcome)


def score_round_part_2(round: str) -> int:
    opponent_code, outcome_code = round.split(" ", maxsplit=2)
    opponent = INPUTS[opponent_code]
    outcome = OUTCOMES[outcome_code]
    response = decide(opponent, outcome)
    return score(response, outcome)


def part_1(data: Iterator[str]) -> int:
    return sum(map(score_round_part_1, data))


def part_2(data: Iterator[str]) -> int:
    return sum(map(score_round_part_2, data))


def main(data: Iterator[str]) -> tuple[int, int]:
    data_1, data_2 = tee(data)
    return (part_1(data_1), part_2(data_2))

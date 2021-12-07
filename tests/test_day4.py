from collections import defaultdict
from typing import DefaultDict

import pytest
import numpy as np

from solutions.day4_bingo import (  # type: ignore
    line_processor,
    play_bingo,
)


@pytest.fixture
def boards_marked_boards_and_numbers() -> tuple[np.ndarray, np.ndarray, list[int]]:
    """
    Returns the boards, marked_boards and numbers
    """
    numbers: list[int] = []
    boards: DefaultDict[int, list[list[int]]] = defaultdict(list)
    n_board: int = -1
    for line in line_processor("tests/test_inputs/day4"):  # type: str
        if "," in line:
            # it is a list of numbers
            numbers.extend(int(i) for i in line.split(","))
        elif not line.strip():
            # it marks the beginning of a board
            n_board += 1
        else:
            row: list[int] = [int(i) for i in line.split()]
            boards[n_board].append(row)

    # create a multidimension array of all the boards
    all_boards: np.ndarray = np.array([i for i in boards.values()])
    # create a copy of that array with zeros everywhere (where a 0
    #  represents not marked) and a 1 will represent marked
    marked_boards: np.ndarray = np.zeros((n_board + 1, 5, 5), dtype=int)

    return all_boards, marked_boards, numbers


def test_find_the_first_winner(boards_marked_boards_and_numbers):
    assert play_bingo(*boards_marked_boards_and_numbers, "first") == 4512


def test_find_the_last_winner(boards_marked_boards_and_numbers):
    assert play_bingo(*boards_marked_boards_and_numbers, "last") == 1924

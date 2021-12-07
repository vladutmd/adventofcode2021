from collections import defaultdict
from typing import DefaultDict, Literal
from contextlib import contextmanager
from typing import IO, ContextManager, Generator, TextIO

import numpy as np


@contextmanager
def file_read(filename: str) -> Generator[TextIO, None, None]:
    f: TextIO = open(filename)
    yield f
    f.close()


def line_processor(filename: str) -> Generator[str, None, None]:
    """
    This generator takes a file line by line
    and processes one by one.
    """
    cm: ContextManager[IO] = file_read(filename)
    with cm as input_file:
        for line in input_file:
            yield line.strip()


def play_bingo(
    boards: np.ndarray,
    marked_boards: np.ndarray,
    numbers: list[int],
    winner: Literal["first", "last"],
) -> int:
    """
    This function will play bingo.
    """

    # the following set will contain the board indices that have finished
    boards_finished: set[int] = set()
    # the following list will contain the numbers that caused a board to win
    winning_numbers: list[int] = list()
    # the following list will contain the sum of the unmarked numbers on the
    # boards that won when they won
    winning_sums: list[int] = list()

    for number in numbers:  # type: int
        # the following set contains the boards which WIN this round
        # this is needed in order to only iterate through these ones and
        # check if they haven't won before
        round_winners: set[int] = set()

        # let's mark the positions where the current NUMBER called is present
        marked_boards = np.where(boards == number, 1, marked_boards)
        # now let's check for winners, first we check the sum of columns
        sum_columns: np.ndarray = marked_boards.sum(axis=1)
        winning_columns: np.ndarray = np.where(sum_columns == 5)
        # (array([2]), array([0])) means board 2, col 0

        # then we check the sum of rows
        sum_rows: np.ndarray = marked_boards.sum(axis=2)
        winning_rows: np.ndarray = np.where(sum_rows == 5)
        # (array([2]), array([0])) means board 2, row 0

        for board_no in winning_columns[0]:  # type: int
            round_winners.add(board_no)
        for board_no in winning_rows[0]:
            round_winners.add(board_no)

        for board_no in round_winners:
            # let's first check this board hasn't already won
            if board_no not in boards_finished:

                boards_finished.add(board_no)
                winning_numbers.append(number)

                # let's find the sum of all the unmarked numbers
                unmarked_numbers: np.ndarray = np.ma.masked_where(
                    marked_boards[board_no], boards[board_no]
                )
                winning_sum: int = unmarked_numbers.sum()
                winning_sums.append(winning_sum)
    if winner == "first":
        return winning_sums[0] * winning_numbers[0]
    elif winner == "last":
        return winning_sums[-1] * winning_numbers[-1]


if __name__ == "__main__":
    numbers: list[int] = []
    boards: DefaultDict[int, list[list[int]]] = defaultdict(list)
    n_board: int = -1
    for line in line_processor("inputs/day4"):  # type: str
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

    # finally let's print the first and the last winning boards:
    # product of the winning number and the winning sum
    print(play_bingo(all_boards, marked_boards, numbers, "first"))
    print(play_bingo(all_boards, marked_boards, numbers, "last"))

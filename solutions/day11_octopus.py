from contextlib import contextmanager
from typing import IO, ContextManager, Generator, TextIO


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


def advance_step(energies: list[list[int]]):
    """
    This function advances on step at a time and
    returns the number of flashes seen in this step.
    """
    flashes: int = 0
    position_stack: list[tuple[int, int]] = []
    n_rows: int = len(energies)
    n_cols: int = len(energies[0])

    # iterate through all the energies
    # row by row, column by column
    for row in range(n_rows):  # type: int
        for col in range(n_cols):  # type: int
            # increase the energy at that location by 1
            energies[row][col] += 1
            # if the energy is greater than 9, increase
            # the number of flashes by 1 and set its new
            # energy level to 0
            if energies[row][col] > 9:
                # we got a flash
                flashes += 1
                # set the new energy to 0
                energies[row][col] = 0
                # add this location to the stack so that
                # we check its neighbours
                position_stack.append((row, col))
    # now let's go through the stack of the positions where
    # there was a flash
    while position_stack:
        # get a position from the stack
        row, col = position_stack.pop()
        # let's look at its neighbours
        neighbours: list[tuple[int, int]] = get_neighbour_pos_changes()
        for pos_change in neighbours:  # type: tuple[int, int]
            d_row: int = pos_change[0]
            d_col: int = pos_change[1]
            new_row: int = row + d_row
            new_col: int = col + d_col
            # check if we are still within bounds and that
            # this location did not flash in this step (i.e.
            # now has an energy of 0)
            if (
                0 <= new_row < n_rows
                and 0 <= new_col < n_cols
                and energies[new_row][new_col] > 0
            ):
                energies[new_row][new_col] += 1
                if energies[new_row][new_col] > 9:
                    # we have a neighbour flash
                    flashes += 1
                    # reset its energy to 0
                    energies[new_row][new_col] = 0
                    # add it to the position stack
                    position_stack.append((new_row, new_col))
    return flashes


def get_neighbour_pos_changes() -> list[tuple[int, int]]:
    up: tuple[int, int] = (-1, 0)
    down: tuple[int, int] = (1, 0)
    left: tuple[int, int] = (0, -1)
    right: tuple[int, int] = (0, 1)
    up_left: tuple[int, int] = (-1, -1)
    up_right: tuple[int, int] = (-1, 1)
    down_left: tuple[int, int] = (1, -1)
    down_right: tuple[int, int] = (1, 1)
    return [up, down, left, right, up_left, up_right, down_left, down_right]


if __name__ == "__main__":
    octopodes: list[list[int]] = [
        list(map(int, row)) for row in line_processor("inputs/day11")
    ]
    part_1_copy: list[list[int]] = [row[:] for row in octopodes]
    part_1_answer: int = sum(advance_step(part_1_copy) for _ in range(100))
    print(part_1_answer)

    part_2_copy: list[list[int]] = [row[:] for row in octopodes]
    n_steps: int = 0
    while sum([sum(row) for row in part_2_copy]) > 0:
        advance_step(part_2_copy)
        n_steps += 1
    print(n_steps)

from contextlib import contextmanager
from typing import IO, ContextManager, Generator, TextIO
from operator import mul


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


def process_instruction(instruction: str) -> tuple[int, int]:
    """
    This functions takes in an instructions succh as "forward 5"
    and returns the corresponding change in position as a Tuple of two
    integers.

    The first one is the change in horizontal position and the second one
    is the change in vertical position.

    Please note that a positive change in vertical positions means you go
    deeper.
    """
    action, str_value = instruction.split()  # type: str, str
    value: int = int(str_value)
    if action == "forward":
        return (+value, 0)
    elif action == "down":
        return (0, +value)
    elif action == "up":
        return (0, -value)
    return (0, 0)


def new_process_instruction(
    instruction: str, pos: tuple[int, int], aim: int
) -> tuple[tuple[int, int], int]:
    """
    This functions takes in an instructions succh as "forward 5"
    and returns the corresponding change in position as a Tuple of two
    integers.

    The first one is the change in horizontal position and the second one
    is the change in vertical position.

    Please note that a positive change in vertical positions means you go
    deeper.
    """

    action, str_value = instruction.split()  # type: str, str
    value: int = int(str_value)

    horiz, vert = pos  # type: int, int

    if action == "forward":
        horiz += value
        vert += aim * value
    elif action == "down":
        aim += value
    elif action == "up":
        aim -= value

    return ((horiz, vert), aim)


if __name__ == "__main__":
    initial_pos: list[int] = [0, 0]
    for line in line_processor("inputs/day2"):
        change: tuple[int, int] = process_instruction(line)
        initial_pos[0] += change[0]
        initial_pos[1] += change[1]
    print(mul(*initial_pos))

    pos: tuple[int, int] = (0, 0)
    aim: int = 0
    for line in line_processor("inputs/day2"):
        pos, aim = new_process_instruction(line, pos, aim)
    print(mul(*pos))

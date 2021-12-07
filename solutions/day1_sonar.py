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


def get_changes(depths: list[int], window_width: int) -> int:
    """
    This function iterates over a list of integers and does a
    moving average sum and compares the N+1th sum with the Nth sum.
    If larger, the changes variable is increased by one.
    """
    new_sum: int = 0
    previous_sum: int = 0
    # start changes as -1 as the first one will be comparing with 0
    # so it's a fake first increment
    changes: int = -1
    for i in range(0, len(depths) - window_width + 1):
        new_sum = sum(depths[i : i + window_width])
        changes += new_sum > previous_sum
        previous_sum = new_sum
    return changes


if __name__ == "__main__":
    depths: list[int] = [int(i) for i in line_processor("inputs/day1")]
    print(get_changes(depths, 1))
    print(get_changes(depths, 3))

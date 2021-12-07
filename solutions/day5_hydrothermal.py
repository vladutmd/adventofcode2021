from collections import defaultdict
from typing import DefaultDict
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


def mark(filename: str, diagonal: bool = False) -> int:
    ocean_floor_map: DefaultDict[tuple[int, int], int] = defaultdict(int)

    # for line in line_processor("tem5"):
    for line in line_processor(filename):
        start, end = line.split(" -> ")  # type: str, str
        x1, y1 = [int(i) for i in start.split(",")]  # type: int, int
        x2, y2 = [int(i) for i in end.split(",")]  # type: int, int
        if x1 != x2 and y1 != y2:
            if diagonal:
                xrange: range = (
                    range(x1, x2 + 1, 1) if x1 <= x2 else range(x1, x2 - 1, -1)
                )
                yrange: range = (
                    range(y1, y2 + 1, 1) if y1 <= y2 else range(y1, y2 - 1, -1)
                )
                for dx, dy in zip(xrange, yrange):  # type: int, int
                    ocean_floor_map[(dx, dy)] += 1
            else:
                continue
        else:
            for dx in range(min(x1, x2), max(x1, x2) + 1):
                for dy in range(min(y1, y2), max(y1, y2) + 1):
                    ocean_floor_map[(dx, dy)] += 1
    return sum(1 for i in ocean_floor_map.values() if i >= 2)


if __name__ == "__main__":
    filename: str = "inputs/day5"
    print(mark(filename=filename, diagonal=False))
    print(mark(filename=filename, diagonal=True))

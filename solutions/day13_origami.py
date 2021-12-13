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


def create_dots_map_and_instructions_list(
    filename: str,
) -> tuple[dict[tuple[int, int], int], list[tuple[str, int]]]:
    # use a dictionary to store the locations of the dots where
    # the key is a tuple of x,y coordinates
    dots: dict[tuple[int, int], int] = {}
    dots_instructions_separator: bool = False
    fold_instructions: list[tuple[str, int]] = []
    for line in line_processor(filename):  # type: str
        # check if line is not empty
        if not line:
            dots_instructions_separator = True
        elif line and dots_instructions_separator:
            axis_and_location: list[str] = line.lstrip(
                "fold along "
            ).split("=")
            axis: str = axis_and_location[0]
            location: int = int(axis_and_location[1])
            fold_instructions.append((axis, location))
        else:
            x, y = [int(i) for i in line.split(",")]  # type: int, int
            dots[(x, y)] = 1

    return dots, fold_instructions


def fold_paper(
    dots: dict[tuple[int, int], int], instruction: tuple[str, int]
) -> dict[tuple[int, int], int]:
    folded_paper_dots: dict[tuple[int, int], int] = {}
    axis, line = instruction  # type: str, int
    for (x, y), _ in dots.items():  # type: tuple[int, int], int
        # if y fold, i.e. horizontal fold, x values stay the same
        # y ones can change
        new_x: int = x if axis == "y" else line - abs(line - x)
        # if x fold, i.e.  vertical fold, y values stay the same,
        # x ones can change
        new_y: int = y if axis == "x" else line - abs(line - y)
        folded_paper_dots[new_x, new_y] = 1
    return folded_paper_dots


def print_dots(dots: dict[tuple[int, int], int]) -> None:
    max_x: int = max(dots.keys(), key=lambda pos: pos[0])[0]
    max_y: int = max(dots.keys(), key=lambda pos: pos[1])[1]
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(dots.get((x, y), "."), end="")
        print(" ")


if __name__ == "__main__":
    dots, fold_instructions = create_dots_map_and_instructions_list(
        "inputs/day13"
    )
    dots = fold_paper(dots, fold_instructions[0])
    part_1: int = sum(dots.values())
    print(part_1)

    for instruction in fold_instructions[1:]:
        dots = fold_paper(dots, instruction)
    print_dots(dots)

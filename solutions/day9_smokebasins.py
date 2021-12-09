from contextlib import contextmanager
from typing import IO, ContextManager, Generator, TextIO, NewType
from math import prod

HeightMap = NewType("HeightMap", dict[tuple[int, int], int])


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


def build_neighbourhood_coordinates(col: int, row: int) -> list[tuple[int, int]]:
    up: tuple[int, int] = (col, row - 1)
    down: tuple[int, int] = (col, row + 1)
    left: tuple[int, int] = (col - 1, row)
    right: tuple[int, int] = (col + 1, row)
    return [up, down, left, right]


def determine_if_low_point(col: int, row: int, height_map: HeightMap) -> bool:
    # if all of the neighbours are higher than the point, it's a low point
    return all(
        height_map.get(neighbour, 9) > height_map[(col, row)]
        for neighbour in build_neighbourhood_coordinates(col, row)
    )


def find_low_points(height_map: HeightMap) -> list[tuple[int, int]]:
    low_points: list[tuple[int, int]] = [
        (col, row)
        for col, row in height_map
        if determine_if_low_point(col, row, height_map)
    ]
    return low_points


def find_risk_level(height_map: HeightMap, col: int, row: int) -> int:
    return 1 + height_map[(col, row)]


def grow_basin(
    col: int, row: int, height_map: HeightMap, existing_basin: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    current_height: int = height_map[(col, row)]
    for neighbour in build_neighbourhood_coordinates(col, row):  # type: tuple[int, int]
        # let's only look at the positions that are higher since we started
        # from the lowest position
        new_height: int = height_map.get(neighbour, 0)
        if new_height > current_height and new_height != 9:  # not in a basin
            existing_basin.add(neighbour)
            existing_basin = grow_basin(*neighbour, height_map, existing_basin)
    return existing_basin


def get_basin(col: int, row: int, height_map: HeightMap):
    basin_members: set[tuple[int, int]] = set()
    basin_members.add((col, row))
    basin_members = grow_basin(col, row, height_map, existing_basin=basin_members)
    return basin_members


if __name__ == "__main__":
    height_map: HeightMap = dict()
    row_number: int = 0
    for row in line_processor("inputs/day9"):
        for column_number, height in enumerate(row):
            height_map[(column_number, row_number)] = int(height)
        row_number += 1
    low_points: list[tuple[int, int]] = find_low_points(height_map)
    print(sum(find_risk_level(height_map, col, row) for col, row in low_points))

    basin_sizes: list[int] = []
    for low_point in low_points:  # typ: tuple[int, int]
        starting_col, starting_row = low_point  # type: int, int
        basin: set[tuple[int, int]] = get_basin(starting_col, starting_row, height_map)
        basin_sizes.append(len(basin))
    print(prod(sorted(basin_sizes)[-3:]))

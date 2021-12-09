import pytest

from math import prod

from solutions.day9_smokebasins import (  # type: ignore
    line_processor,
    find_low_points,
    find_risk_level,
    get_basin,
    HeightMap,
)


@pytest.fixture
def height_map() -> HeightMap:
    """
    Returns the height map.
    """
    height_map: HeightMap = dict()
    row_number: int = 0
    for row in line_processor("tests/test_inputs/day9"):
        for column_number, height in enumerate(row):
            height_map[(column_number, row_number)] = int(height)
        row_number += 1
    return height_map


@pytest.fixture
def low_points(height_map: HeightMap) -> list[tuple[int, int]]:
    low_points: list[tuple[int, int]] = find_low_points(height_map)
    return low_points


def test_find_risk_level(height_map: HeightMap, low_points: list[tuple[int, int]]):
    assert sum(find_risk_level(height_map, col, row) for col, row in low_points) == 15


def test_get_basin(height_map: HeightMap, low_points: list[tuple[int, int]]):
    basin_sizes: list[int] = []
    for low_point in low_points:  # typ: tuple[int, int]
        starting_col, starting_row = low_point  # type: int, int
        basin: set[tuple[int, int]] = get_basin(starting_col, starting_row, height_map)
        basin_sizes.append(len(basin))
    assert prod(sorted(basin_sizes)[-3:]) == 1134

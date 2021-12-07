import pytest

from solutions.day7_crabs import (  # type: ignore
    line_processor,
    find_fuel_cost,
    find_distances_from_median,
    find_increasing_distances_from_mean,
)


@pytest.fixture
def crabs() -> list[int]:
    """
    Returns the initial crab positions.
    """
    crabs: list[int] = [
        int(i)
        for i in [line for line in line_processor("tests/test_inputs/day7")]
        .pop()
        .split(",")
    ]
    return crabs


def test_median_distance(crabs: list[int]):
    assert find_fuel_cost(crabs, "median", find_distances_from_median) == 37


def test_increasing_mean_distance(crabs: list[int]):
    assert find_fuel_cost(crabs, "mean", find_increasing_distances_from_mean) == 170

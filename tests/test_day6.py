import pytest

from solutions.day6_lanternfish import (  # type: ignore
    line_processor,
    stalk_the_fish_society,
)


@pytest.fixture
def fish() -> list[int]:
    """
    Returns the initial fish states.
    """
    fish: list[int] = [
        int(i)
        for i in [line for line in line_processor("tests/test_inputs/day6")]
        .pop()
        .split(",")
    ]
    return fish


def test_stalking_around_the_world_in_80_days(fish: list[int]):
    assert stalk_the_fish_society(fish, 80) == 5934


def test_stalking_around_the_world_in_2_pow_8(fish: list[int]):
    assert stalk_the_fish_society(fish, 256) == 26984457539

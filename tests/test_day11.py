import pytest

from solutions.day11_octopus import (  # type: ignore
    line_processor,
    advance_step,
)


@pytest.fixture
def octopodes() -> list[list[int]]:
    """
    Returns the octopodes' energies.
    """
    octopodes: list[list[int]] = [
        list(map(int, row)) for row in
        line_processor("tests/test_inputs/day11")
    ]
    return octopodes


def test_part_1(octopodes: list[list[int]]):
    assert sum(advance_step(octopodes) for _ in range(100)) == 1656


def test_part_2(octopodes: list[list[int]]):
    n_steps: int = 0
    while sum([sum(row) for row in octopodes]) > 0:
        advance_step(octopodes)
        n_steps += 1
    assert n_steps == 195

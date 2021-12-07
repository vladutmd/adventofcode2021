import pytest

from solutions.day5_hydrothermal import mark  # type: ignore


@pytest.fixture
def filename() -> str:
    """
    Returns the test input filename.
    """
    return "tests/test_inputs/day5"


def test_mark_vents_no_diagonal(filename):
    assert mark(filename, diagonal=False) == 5


def test_mark_vents_with_diagonal(filename):
    assert mark(filename, diagonal=True) == 12

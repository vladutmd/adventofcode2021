import pytest

from solutions.day1_sonar import get_changes, line_processor  # type: ignore


@pytest.fixture
def input_list() -> list[int]:
    """
    Returns the test list of entries.
    """
    return [int(i) for i in line_processor("tests/test_inputs/day1")]


def test_get_changes(input_list):
    depths: list[int] = input_list
    assert get_changes(depths, 1) == 7
    assert get_changes(depths, 3) == 5

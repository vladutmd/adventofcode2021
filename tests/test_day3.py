import pytest

from solutions.day3_diagnostic import (  # type: ignore
    line_processor,
    find_gamma_and_epsilon_product,
    find_life_support_rating,
)


@pytest.fixture
def input_list_and_n_bits() -> tuple[list[int], int]:
    """
    Returns the test list of numbers.
    """
    numbers: list[int] = []
    n_bits: int = 0
    for line in line_processor("tests/test_inputs/day3"):
        n_bits = max(len(line.strip()), n_bits)
        numbers.append(int(line.strip(), 2))
    return numbers, n_bits


def test_find_gamma_and_epsilon_product(input_list_and_n_bits):
    numbers: list[int]
    n_bits: int
    numbers, n_bits = input_list_and_n_bits
    assert find_gamma_and_epsilon_product(numbers, n_bits) == 198


def test_find_life_support_rating(input_list_and_n_bits):
    numbers: list[int]
    n_bits: int
    numbers, n_bits = input_list_and_n_bits
    assert find_life_support_rating(numbers, n_bits) == 230

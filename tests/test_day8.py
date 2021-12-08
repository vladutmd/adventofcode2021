import pytest

from solutions.day8_segments import (  # type: ignore
    line_processor,
    process_digits,
)


@pytest.fixture
def display_readings() -> list[list[list[str]]]:
    """
    Returns the display readings.
    """
    data: list[list[list[str]]] = []
    for line in line_processor("tests/test_inputs/day8"):  # type: str
        left_side, right_side = line.split(" | ")  # type: str, str
        left_letters: list[str] = ["".join(sorted(word)) for word in left_side.split()]
        right_letters: list[str] = [
            "".join(sorted(word)) for word in right_side.split()
        ]
        data.append([left_letters, right_letters])
    return data


def test_process_digits(display_readings: list[list[list[str]]]):
    digit_appearances_part_1: int = 0
    sum_four_digits_part_2: int = 0
    for ten_numbers, four_digits in display_readings:
        part1, part2 = process_digits(ten_numbers, four_digits)  # type: int, int
        digit_appearances_part_1 += part1
        sum_four_digits_part_2 += part2

    assert digit_appearances_part_1 == 26
    assert sum_four_digits_part_2 == 61229

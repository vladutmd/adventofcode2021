import pytest

from operator import mul

from solutions.day2_pilot import (  # type: ignore
    line_processor,
    process_instruction,
    new_process_instruction,
)


@pytest.fixture
def input_list() -> list[str]:
    """
    Returns the test list of instructions.
    """
    return [line for line in line_processor("tests/test_inputs/day2")]


def test_process_instruction(input_list):
    instructions: list[str] = input_list
    initial_pos: list[int] = [0, 0]
    for line in instructions:
        change: tuple[int, int] = process_instruction(line)
        initial_pos[0] += change[0]
        initial_pos[1] += change[1]
    assert mul(*initial_pos) == 150


def test_new_process_instruction(input_list):
    instructions: list[str] = input_list
    pos: tuple[int, int] = (0, 0)
    aim: int = 0
    for line in instructions:
        pos, aim = new_process_instruction(line, pos, aim)
    assert mul(*pos) == 900

import pytest

from solutions.day13_origami import (  # type: ignore
    create_dots_map_and_instructions_list,
    fold_paper,
)


@pytest.fixture
def dots_and_instructions() -> tuple[dict[tuple[int, int], int], list[tuple[str, int]]]:
    """
    Returns the dots map and fold instructions.
    """
    dots, fold_instructions = create_dots_map_and_instructions_list(
        "tests/test_inputs/day13"
    )
    return dots, fold_instructions


def test_part_1_answer(dots_and_instructions):
    dots, fold_instructions = dots_and_instructions
    dots = fold_paper(dots, fold_instructions[0])
    part_1: int = sum(dots.values())
    assert part_1 == 17

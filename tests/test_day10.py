import pytest

from solutions.day10_syntax import (  # type: ignore
    line_processor,
    determine_score_of_line,
)


@pytest.fixture
def lines() -> list[str]:
    """
    Returns the list of lines.
    """
    lines: list[str] = [line for line in line_processor("tests/test_inputs/day10")]
    return lines


@pytest.fixture
def closing_brackets() -> dict[str, str]:
    closing_brackets: dict[str, str] = {")": "(", "]": "[", "}": "{", ">": "<"}
    return closing_brackets


@pytest.fixture
def part1_scoremap() -> dict[str, int]:
    score_map: dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return score_map


@pytest.fixture
def part2_scoremap() -> dict[str, int]:
    score_map = {"(": 1, "[": 2, "{": 3, "<": 4}
    return score_map


def test_corrupted_lines_score(
    lines: list[str],
    part1_scoremap: dict[str, int],
    closing_brackets: dict[str, str],
):
    total_score: int = 0
    for line in lines:  # type: str
        line_score: int = determine_score_of_line(
            line, part1_scoremap, closing_brackets, corrupted=True, incomplete=False
        )
        total_score += line_score
    assert total_score == 26397


def test_incomplete_lines_score(
    lines: list[str],
    part2_scoremap: dict[str, int],
    closing_brackets: dict[str, str],
):
    scores: list[int] = []
    for line in lines:
        line_score = determine_score_of_line(
            line, part2_scoremap, closing_brackets, corrupted=False, incomplete=True
        )
        if line_score != 0:
            scores.append(line_score)
    n_scores: int = len(scores)
    median_score: int = sorted(scores)[n_scores // 2]
    assert median_score == 288957

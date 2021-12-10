from contextlib import contextmanager
from typing import IO, ContextManager, Generator, TextIO


@contextmanager
def file_read(filename: str) -> Generator[TextIO, None, None]:
    f: TextIO = open(filename)
    yield f
    f.close()


def line_processor(filename: str) -> Generator[str, None, None]:
    """
    This generator takes a file line by line
    and processes one by one.
    """
    cm: ContextManager[IO] = file_read(filename)
    with cm as input_file:
        for line in input_file:
            yield line.strip()


def determine_score_of_line(
    line: str,
    score_map: dict[str, int],
    closing_brackets: dict[str, str],
    corrupted: bool,
    incomplete: bool,
) -> int:
    score: int = 0
    bracket_stack: list[str] = []
    for bracket in line:  # type: str
        if bracket not in closing_brackets:
            # i.e. if it's an opening bracket, then let's
            # add it to the stack
            bracket_stack.append(bracket)
        # if not true, it must be a closing bracket
        # let's see if it matches with the last one
        elif bracket_stack.pop() != closing_brackets[bracket]:
            if corrupted:
                score = score_map[bracket]
            break
    else:
        if incomplete:
            for bracket in bracket_stack[::-1]:
                score *= 5
                score += score_map[bracket]
    return score


if __name__ == "__main__":

    lines: list[str] = [line for line in line_processor("inputs/day10")]

    score_map: dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
    closing_brackets: dict[str, str] = {")": "(", "]": "[", "}": "{", ">": "<"}

    total_score: int = 0
    for line in lines:  # type: str
        line_score: int = determine_score_of_line(
            line, score_map, closing_brackets, corrupted=True, incomplete=False
        )
        total_score += line_score

    print(total_score)

    score_map = {"(": 1, "[": 2, "{": 3, "<": 4}
    scores: list[int] = []
    for line in lines:
        line_score = determine_score_of_line(
            line, score_map, closing_brackets, corrupted=False, incomplete=True
        )
        if line_score != 0:
            scores.append(line_score)
    n_scores: int = len(scores)
    median_score: int = sorted(scores)[n_scores // 2]
    print(median_score)

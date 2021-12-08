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


def determine_mapping(ten_numbers: list[str]) -> dict[str, int]:
    one: str = [pattern for pattern in ten_numbers if len(pattern) == 2].pop()
    four: str = [pattern for pattern in ten_numbers if len(pattern) == 4].pop()
    seven: str = [pattern for pattern in ten_numbers if len(pattern) == 3].pop()
    eight: str = [pattern for pattern in ten_numbers if len(pattern) == 7].pop()
    nine: str = [
        pattern
        for pattern in ten_numbers
        if len(pattern) == 6 and all(letter in pattern for letter in four)
    ].pop()
    zero: str = [
        pattern
        for pattern in ten_numbers
        if len(pattern) == 6
        and pattern != nine
        and all(letter in pattern for letter in one)
    ].pop()
    six: str = [
        pattern
        for pattern in ten_numbers
        if len(pattern) == 6
        if (pattern != nine and pattern != zero)
    ].pop()
    three: str = [
        pattern
        for pattern in ten_numbers
        if len(pattern) == 5 and all(letter in pattern for letter in one)
    ].pop()
    five: str = [
        pattern
        for pattern in ten_numbers
        if len(pattern) == 5
        and pattern != three
        and all(letter in nine for letter in pattern)
    ].pop()
    two: str = [
        pattern
        for pattern in ten_numbers
        if len(pattern) == 5 and pattern != five and pattern != three
    ].pop()

    string_to_numbers: dict[str, int] = {
        zero: 0,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8,
        nine: 9,
    }
    return string_to_numbers


def process_digits(ten_numbers: list[str], four_digits: list[str]) -> tuple[int, int]:
    number_dict: dict[str, int] = determine_mapping(ten_numbers)
    part1: int = sum(
        True for string in four_digits if number_dict[string] in [1, 4, 7, 8]
    )
    part2: int = int("".join(str(number_dict[pattern]) for pattern in four_digits))
    return part1, part2


if __name__ == "__main__":
    data: list[list[list[str]]] = []
    for line in line_processor("inputs/day8"):  # type: str
        left_side, right_side = line.split(" | ")  # type: str, str
        left_letters: list[str] = ["".join(sorted(word)) for word in left_side.split()]
        right_letters: list[str] = [
            "".join(sorted(word)) for word in right_side.split()
        ]
        data.append([left_letters, right_letters])

    digit_appearances_part_1: int = 0
    sum_four_digits_part_2: int = 0
    for ten_numbers, four_digits in data:
        part1, part2 = process_digits(ten_numbers, four_digits)  # type: int, int
        digit_appearances_part_1 += part1
        sum_four_digits_part_2 += part2

    print(digit_appearances_part_1)
    print(sum_four_digits_part_2)

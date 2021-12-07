from operator import ge, lt
from typing import Callable, Union
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


def find_gamma_and_epsilon_product(numbers: list[int], n_bits: int) -> int:

    gamma: list[int] = [0 for i in range(n_bits)]
    epsilon: list[int] = [0 for i in range(n_bits)]
    half: int = len(numbers) // 2
    operator: Callable[[int, int], bool] = ge
    for bit_shift in range(n_bits - 1, -1, -1):  # type: int
        digit_result: int = sum((int(j) >> bit_shift) & 1 for j in numbers)
        most_common: int = 1 if operator(digit_result, half) else 0
        gamma.append(most_common)
        epsilon.append(int(not most_common))
    gamma_int: int = int("".join(str(i) for i in gamma), 2)
    epsilon_int: int = int("".join(str(i) for i in epsilon), 2)
    return gamma_int * epsilon_int


def find_life_support_rating(numbers: list[int], n_bits: int) -> int:
    def _find_rating(
        numbers: list[int],
        n_bits: int,
        operator: Callable[[int, Union[int, float]], bool],
    ) -> int:
        # this function can be used to find both the oxygen and co2 rating

        # create a set containing the original numbers at the start
        # of the iteration. This set will be overwritten at the end
        # of an iteration
        initial_numbers: set[int] = set(numbers)
        for bit_shift in range(n_bits - 1, -1, -1):  # type: int
            current_numbers: set[int] = set(i for i in initial_numbers)
            half: float = len(initial_numbers) / 2
            digit_result: int = sum(
                (int(j) >> bit_shift) & 1 for j in initial_numbers
            )
            most_common: int = 1 if operator(digit_result, half) else 0
            if len(current_numbers) == 1:
                break

            for number in initial_numbers:  # type: int
                if ((number >> bit_shift) & 1) != most_common:
                    current_numbers.discard(number)
            initial_numbers = set(i for i in current_numbers)
        return current_numbers.pop()

    oxygen: int = _find_rating(numbers, n_bits, ge)
    co2: int = _find_rating(numbers, n_bits, lt)
    return oxygen * co2


if __name__ == "__main__":
    numbers: list[int] = []
    n_bits: int = 0
    for line in line_processor("inputs/day3"):
        n_bits = max(len(line.strip()), n_bits)
        numbers.append(int(line.strip(), 2))

    print(find_gamma_and_epsilon_product(numbers, n_bits))
    print(find_life_support_rating(numbers, n_bits))

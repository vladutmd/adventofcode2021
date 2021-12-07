from contextlib import contextmanager
from typing import IO, Callable, ContextManager, Generator, Literal, TextIO


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


def find_fuel_cost(
    crabs: list[int],
    central_position: Literal["median", "mean"],
    fuel_function: Callable[[list[int]], int],
) -> int:
    n_crabs: int = len(crabs)
    central: int
    if central_position == "median":
        crabs = sorted(crabs)
        # calculate the median after sorting these crabs
        central = crabs[int(n_crabs / 2)]
    elif central_position == "mean":
        central = int(sum(crabs) / n_crabs)
    distances: list[int] = [abs(crab_pos - central) for crab_pos in crabs]
    fuel_cost: int = fuel_function(distances)
    return fuel_cost


def find_distances_from_median(crab_distances: list[int]) -> int:
    # for each one, let's find out how far they are from the median position
    # why median? because distances close and far are worth the same,
    # so many small distances cancel out the few big distances
    fuel_cost: int = sum(crab_distances)
    return fuel_cost


def find_increasing_distances_from_mean(crab_distances: list[int]) -> int:
    # let's find the distances from the mean. why mean? the values far aay need
    # a lot more fuel so we want to rduce their movements. consequently, we
    # find the mean of all the values
    fuel_cost: int = int(sum([i * (i + 1) / 2 for i in crab_distances]))
    return fuel_cost


if __name__ == "__main__":
    crabs: list[int] = [
        int(i) for i in [line for line in line_processor("tem")].pop().split(",")
    ]
    print(find_fuel_cost(crabs, "median", find_distances_from_median))
    print(find_fuel_cost(crabs, "mean", find_increasing_distances_from_mean))

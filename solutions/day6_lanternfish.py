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


def stalk_the_fish_society(fish: list[int], stalking_period: int) -> int:
    # let's keep track of how many fish are in each state on each day
    # there are 9 states 0, 1, 2, ..., 7, 8
    states: list[int] = [0 for _ in range(9)]
    # now let's set the initial states
    # for example if the initial state is 3, 4, 3, 1, 2
    # there are two fish in state 3, one in 1, one in 2, one in 4
    for initial_state in fish:  # type: int
        states[initial_state] += 1

    # ok now let's simulate the day
    for _ in range(stalking_period):
        # let's look at how many are in state 0 as those create a new fish
        # i.e. a new fish in state 8
        fish_in_labour: int = states[0]
        # now all the fish in state 1 become state 0, state 2 become state 1,
        # ... state 7 becomes state 6
        # i.e. we shift states 1:7 (inclusive) to the left
        for state in range(0, 8):  # type: int
            states[state] = states[state + 1]
        # after finishing labour, the state 0 fish give birth or buy new fish
        # off a popular retail website that will surely start delivering
        # within 1 day to any ocean depth soon enough. those new fish will
        # have a state of 8 but the parent fish will go to a state of 6
        states[6] += fish_in_labour
        states[8] = fish_in_labour
    return sum(states)


if __name__ == "__main__":
    fish: list[int] = [
        int(i)
        for i in [line for line in line_processor("inputs/day6")].pop().split(",")
    ]
    print(stalk_the_fish_society(fish, 80))
    print(stalk_the_fish_society(fish, 256))

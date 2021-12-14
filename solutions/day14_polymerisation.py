from collections import Counter
from contextlib import contextmanager
from itertools import tee
from typing import IO, ContextManager, Generator, TextIO, Iterator


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


def split_into_pairs(polymer_template: str):
    a, b = tee(polymer_template)  # type: Iterator[str], Iterator[str]
    next(b, None)
    return list(f"{i}{j}" for i, j in zip(a, b))


def polymerise(
    initial_pair_counter: Counter, pair_insertion_rules: dict[str, str], n_steps: int
) -> Counter:
    """
    This runs the polymerisation reaction for n_steps.
    """
    # at each step we want to count how many pairs we have
    # and if it matches any rules
    # so if we have NN, we insert a C between, so we increase
    # the counter for pairs NC, CN by 1
    # we have to overwrite the counter at each step

    for _ in range(n_steps):
        current_step_counter: Counter = Counter()
        for pair in initial_pair_counter:  # type: str
            left_element: str = pair[0]
            right_element: str = pair[1]
            # let's check what the middle element should be
            middle_element: str = pair_insertion_rules[pair]
            # now we have two new pairs
            # the count of each one is incremented by
            # what the count of the original pair was
            current_step_counter[left_element + middle_element] += initial_pair_counter[
                pair
            ]
            current_step_counter[
                middle_element + right_element
            ] += initial_pair_counter[pair]
        initial_pair_counter = current_step_counter
    return initial_pair_counter


def count_characters(pair_counter: Counter, initial_polymer_template: str) -> Counter:
    character_counter: Counter = Counter()
    for pair, pair_count in pair_counter.items():
        # let's increment the count of the left element by 1
        left_element, _ = pair  # type: str, str
        character_counter[left_element] += pair_count
    # we also need to manually increment the count of the final element
    # because it's the right side of a pair so we never see it
    character_counter[initial_polymer_template[-1]] += 1
    return character_counter


if __name__ == "__main__":
    polymer_template: str = ""
    pair_insertion_rules: dict[str, str] = {}
    for line in line_processor("inputs/day14"):
        if not line:
            pass
        elif "->" in line:
            pair, insertion = line.split(" -> ")  # type: str, str
            pair_insertion_rules[pair] = insertion
        else:
            polymer_template = line

    # before we start, let's have a list of 2 element fragments/pairs
    # in Python 3.10, can use itertools.pairwise....
    # in 3.9, nope
    list_of_pairs: list[str] = split_into_pairs(polymer_template)
    pair_counter: Counter = Counter(list_of_pairs)

    pair_counter_after_10_steps: Counter = polymerise(
        initial_pair_counter=pair_counter,
        pair_insertion_rules=pair_insertion_rules,
        n_steps=10,
    )
    character_counter_after_10_steps: Counter = count_characters(
        pair_counter=pair_counter_after_10_steps,
        initial_polymer_template=polymer_template,
    )
    part_1: int = max(character_counter_after_10_steps.values()) - min(
        character_counter_after_10_steps.values()
    )
    print(part_1)

    # let's run it for another 30 steps using the current counter
    pair_counter_after_40_steps: Counter = polymerise(
        initial_pair_counter=pair_counter_after_10_steps,
        pair_insertion_rules=pair_insertion_rules,
        n_steps=30,
    )
    character_counter_after_40_steps: Counter = count_characters(
        pair_counter=pair_counter_after_40_steps,
        initial_polymer_template=polymer_template,
    )
    part_2: int = max(character_counter_after_40_steps.values()) - min(
        character_counter_after_40_steps.values()
    )
    print(part_2)

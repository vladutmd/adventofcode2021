import pytest
from collections import Counter

from solutions.day14_polymerisation import (  # type: ignore
    line_processor,
    split_into_pairs,
    polymerise,
    count_characters,
)


@pytest.fixture
def polymer_template_and_insertion_rules() -> tuple[str, dict[str, str]]:
    """
    Returns the initial polymer template and pair insertin rules.
    """
    polymer_template: str = ""
    pair_insertion_rules: dict[str, str] = {}
    for line in line_processor("tests/test_inputs/day14"):
        if not line:
            pass
        elif "->" in line:
            pair, insertion = line.split(" -> ")  # type: str, str
            pair_insertion_rules[pair] = insertion
        else:
            polymer_template = line
    return polymer_template, pair_insertion_rules


def test_part_1_and_2_answers(
    polymer_template_and_insertion_rules: tuple[str, dict[str, str]]
):
    polymer_template, pair_insertion_rules = polymer_template_and_insertion_rules
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
    assert part_1 == 1588

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
    assert part_2 == 2188189693529

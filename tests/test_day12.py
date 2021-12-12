from collections import defaultdict
from typing import Callable
import pytest

from solutions.day12_passage import (  # type: ignore
    line_processor,
    create_graph_from_cave_connections,
    depth_first_search,
    depth_first_search_with_single_small_cave_once,
)


@pytest.fixture
def list_of_cave_connections() -> Callable[[str], list[str]]:
    def _make_connections(input_file: str) -> list[str]:
        """
        Returns the list of cave connections.
        """
        cave_connections: list[str] = [line for line in line_processor(input_file)]
        return cave_connections

    return _make_connections


@pytest.mark.parametrize(
    "filename, part_1_answer, part_2_answer",
    [
        (
            "tests/test_inputs/day12_1",
            10,
            36,
        ),
        (
            "tests/test_inputs/day12_2",
            19,
            103,
        ),
        (
            "tests/test_inputs/day12_3",
            226,
            3509,
        ),
    ],
)
def test_check_loading_connections(
    list_of_cave_connections: Callable[[str], list[str]],
    filename: str,
    part_1_answer: int,
    part_2_answer: int,
):
    cave_connections: list[str] = list_of_cave_connections(filename)
    graph: defaultdict[str, set[str]] = create_graph_from_cave_connections(
        cave_connections
    )
    part_1: int = depth_first_search(
        starting_vertex="start", vertices_seen={"start"}, graph=graph
    )
    part_2: int = depth_first_search_with_single_small_cave_once(
        starting_vertex="start",
        vertices_seen={"start"},
        graph=graph,
        visited_small_cave=True,
    )
    assert part_1 == part_1_answer
    assert part_2 == part_2_answer

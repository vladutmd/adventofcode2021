from collections import defaultdict
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


def create_graph_from_cave_connections(
    cave_connections: list[str],
) -> defaultdict[str, set[str]]:
    # create a graph using a defaultdict where the key is the starting vertex
    # and the value is a set of possible nodes to travel to
    graph: defaultdict[str, set[str]] = defaultdict(set)
    for connection in cave_connections:
        starting_vertex: str
        ending_vertex: str
        starting_vertex, ending_vertex = connection.split("-")
        graph[starting_vertex].add(ending_vertex)
        graph[ending_vertex].add(starting_vertex)
    return graph


def depth_first_search(
    starting_vertex: str,
    vertices_seen: set[str],
    graph: defaultdict[str, set[str]],
):
    if starting_vertex == "end":
        # if this new path starts at end, don't look for further ones
        return 1  # why?

    n_paths: int = 0
    # iterate through the possible vertices we can travel to
    for next_vertex in graph[starting_vertex]:  # type: str
        if next_vertex not in vertices_seen:
            # is it a big cave (UPPER) or small cave (lower)?
            # if big cave, don't add it to the vertices_seen since we
            # can visit it multiple times. only add the small caves
            # to the seen vertices
            # then repeat the process starting at the next_vertex
            if not next_vertex.isupper():
                n_paths += depth_first_search(
                    starting_vertex=next_vertex,
                    vertices_seen=vertices_seen.union({next_vertex}),
                    graph=graph,
                )
            else:
                n_paths += depth_first_search(
                    starting_vertex=next_vertex,
                    vertices_seen=vertices_seen,
                    graph=graph,
                )
    return n_paths


def depth_first_search_with_single_small_cave_once(
    starting_vertex: str,
    vertices_seen: set[str],
    graph: defaultdict[str, set[str]],
    visited_small_cave: bool,
):
    if starting_vertex == "end":
        # if this new path starts at end, don't look for further ones
        # as we care about the paths that end here
        # and it cannot be visited ore than once
        return 1  # why?

    n_paths: int = 0
    # iterate through the possible vertices we can travel to
    for next_vertex in graph[starting_vertex]:  # type: str
        if next_vertex not in vertices_seen:
            # is it a big cave (UPPER) or small cave (lower)?
            # if big cave, don't add it to the vertices_seen since we
            # can visit it multiple times. only add the small caves
            # to the seen vertices
            # then repeat the process starting at the next_vertex
            if not next_vertex.isupper():
                n_paths += depth_first_search_with_single_small_cave_once(
                    starting_vertex=next_vertex,
                    vertices_seen=vertices_seen.union({next_vertex}),
                    graph=graph,
                    visited_small_cave=visited_small_cave,
                )
            else:
                n_paths += depth_first_search_with_single_small_cave_once(
                    starting_vertex=next_vertex,
                    vertices_seen=vertices_seen,
                    graph=graph,
                    visited_small_cave=visited_small_cave,
                )
        # if we can visit caves more than once, then we will start at this cave
        # and call depth_first_search again but this time with visited_small_cave = False
        # since this small cave can only be visited once
        elif visited_small_cave and next_vertex != "start":
            n_paths += depth_first_search_with_single_small_cave_once(
                starting_vertex=next_vertex,
                vertices_seen=vertices_seen,
                graph=graph,
                visited_small_cave=False,
            )

    return n_paths


if __name__ == "__main__":
    cave_connections: list[str] = [line for line in line_processor("inputs/day12")]
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
    print(part_1)
    print(part_2)

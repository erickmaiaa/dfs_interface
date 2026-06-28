import sys
from enum import Enum
from typing import Any


class EdgeType(str, Enum):
    TREE = "Tree"
    BACK = "Back"
    FORWARD = "Forward"
    CROSS = "Cross"


class VertexColor(str, Enum):
    WHITE = "white"
    GRAY = "gray"
    BLACK = "black"


def perform_dfs(
    adj_list: list[list[int]],
    start_vertices: list[int],
    num_vertices: int,
) -> tuple[dict[tuple[int, int], EdgeType], list[int], list[int]]:
    """Run DFS on a directed graph, returning edge classifications and timestamps.

    Visits vertices in start_vertices order first (highest outdegree first),
    then any remaining unvisited vertices in index order.
    """
    discovery_times: list[int] = [0] * num_vertices
    finish_times: list[int] = [0] * num_vertices
    colors: list[VertexColor] = [VertexColor.WHITE] * num_vertices
    edge_types: dict[tuple[int, int], EdgeType] = {}
    time_stamp: list[int] = [0]  # mutable container to avoid nonlocal in iterative version

    visit_order = _build_visit_order(start_vertices, num_vertices)

    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, num_vertices * 2 + 100))
    try:
        for u in visit_order:
            if colors[u] == VertexColor.WHITE:
                _dfs_visit(u, adj_list, colors, discovery_times, finish_times, edge_types, time_stamp)
    finally:
        sys.setrecursionlimit(old_limit)

    return edge_types, discovery_times, finish_times


def _build_visit_order(start_vertices: list[int], num_vertices: int) -> list[int]:
    """Merge priority vertices with remaining ones, preserving uniqueness and order."""
    seen: set[int] = set(start_vertices)
    remaining = [v for v in range(num_vertices) if v not in seen]
    return list(start_vertices) + remaining


def _dfs_visit(
    u: int,
    adj_list: list[list[int]],
    colors: list[VertexColor],
    discovery_times: list[int],
    finish_times: list[int],
    edge_types: dict[tuple[int, int], EdgeType],
    time_stamp: list[int],
) -> None:
    colors[u] = VertexColor.GRAY
    time_stamp[0] += 1
    discovery_times[u] = time_stamp[0]

    for v in adj_list[u]:
        edge = (u, v)
        if colors[v] == VertexColor.WHITE:
            edge_types[edge] = EdgeType.TREE
            _dfs_visit(v, adj_list, colors, discovery_times, finish_times, edge_types, time_stamp)
        elif colors[v] == VertexColor.GRAY:
            edge_types[edge] = EdgeType.BACK
        else:
            if discovery_times[u] < discovery_times[v]:
                edge_types[edge] = EdgeType.FORWARD
            else:
                edge_types[edge] = EdgeType.CROSS

    colors[u] = VertexColor.BLACK
    time_stamp[0] += 1
    finish_times[u] = time_stamp[0]

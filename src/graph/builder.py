from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import networkx as nx


@dataclass
class GraphData:
    graph: nx.DiGraph
    num_vertices: int
    adj_list: list[list[int]]
    vertices_by_outdegree: list[int]  # highest outdegree first

    @property
    def start_node(self) -> int:
        return self.vertices_by_outdegree[0] if self.vertices_by_outdegree else 0


def build_graph_from_file(file_path: str | Path) -> GraphData:
    """Parse a directed graph file and return a GraphData instance.

    File format:
        Line 0: <num_vertices> <num_edges> [D]
        Lines 1..N: <source> <target>
    """
    path = Path(file_path)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Graph file not found: {path}")

    if not lines:
        raise ValueError("Graph file is empty.")

    num_vertices, num_edges = _parse_header(lines[0])

    if num_vertices <= 0:
        raise ValueError("Graph must have at least one vertex.")

    edges, outdegree_counts = _parse_edges(lines[1:], num_edges, num_vertices)

    adj_list: list[list[int]] = [[] for _ in range(num_vertices)]
    for u, v in edges:
        adj_list[u].append(v)

    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_vertices))
    graph.add_edges_from(edges)

    vertices_by_outdegree = _sort_by_outdegree(outdegree_counts, num_vertices)

    return GraphData(
        graph=graph,
        num_vertices=num_vertices,
        adj_list=adj_list,
        vertices_by_outdegree=vertices_by_outdegree,
    )


def _parse_header(line: str) -> tuple[int, int]:
    parts = line.split()
    if len(parts) < 2:
        raise ValueError("First line must contain at least: num_vertices num_edges")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError(f"Invalid header values: '{line.strip()}'")


def _parse_edges(
    edge_lines: list[str],
    expected_count: int,
    num_vertices: int,
) -> tuple[list[tuple[int, int]], Counter]:
    available = min(expected_count, len(edge_lines))
    if available < expected_count:
        import warnings
        warnings.warn(
            f"File has {available} edge lines but header declares {expected_count}. "
            "Processing available lines.",
            stacklevel=3,
        )

    edges: list[tuple[int, int]] = []
    outdegree_counts: Counter = Counter()

    for i, raw_line in enumerate(edge_lines[:available], start=2):
        parts = raw_line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid edge format on line {i}: '{raw_line.strip()}'")
        try:
            u, v = int(parts[0]), int(parts[1])
        except ValueError:
            raise ValueError(f"Non-integer vertex on line {i}: '{raw_line.strip()}'")

        if not (0 <= u < num_vertices and 0 <= v < num_vertices):
            raise ValueError(
                f"Vertex index out of range [0, {num_vertices - 1}] on line {i}: {u} {v}"
            )

        edges.append((u, v))
        outdegree_counts[u] += 1

    return edges, outdegree_counts


def _sort_by_outdegree(outdegree_counts: Counter, num_vertices: int) -> list[int]:
    """Return all vertex indices sorted by outdegree descending, ties broken by index."""
    return sorted(range(num_vertices), key=lambda v: (-outdegree_counts.get(v, 0), v))

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from src.algorithms.dfs import EdgeType


class _NodeColor:
    UNVISITED = "lightgray"
    ACTIVE = "gold"
    FINISHED = "steelblue"


class DfsVisualizer:
    """Drives a step-by-step matplotlib animation of a DFS execution."""

    def __init__(
        self,
        graph: nx.DiGraph,
        start_node: int,
        edge_types: dict[tuple[int, int], EdgeType],
        d_times: list[int],
        f_times: list[int],
        pause_duration: float = 1.0,
    ) -> None:
        self.graph = graph
        self.start_node = start_node
        self.edge_types = edge_types
        self.d_times = d_times
        self.f_times = f_times
        self.pause_duration = pause_duration

        self.pos = nx.spring_layout(graph) if graph.number_of_nodes() > 0 else {}
        self.node_colors = [_NodeColor.UNVISITED] * graph.number_of_nodes()
        self.current_d_times = [0] * graph.number_of_nodes()
        self.current_f_times = [0] * graph.number_of_nodes()
        self._current_time = 0

        plt.figure(figsize=(10, 8))
        self._draw("Initial State")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_animation(self) -> None:
        n = self.graph.number_of_nodes()
        if not (0 <= self.start_node < n):
            print(f"Warning: invalid start node ({self.start_node}). No animation shown.")
        else:
            if self.node_colors[self.start_node] == _NodeColor.UNVISITED:
                self._animate_subtree(self.start_node)

        self._draw("DFS Complete")
        plt.show()

    # ------------------------------------------------------------------
    # Animation helpers
    # ------------------------------------------------------------------

    def _animate_subtree(self, node: int) -> None:
        self.node_colors[node] = _NodeColor.ACTIVE
        self._record_time(node, is_discovery=True)
        self._draw(f"Visiting node {node}  (d={self.current_d_times[node]})")

        for neighbor in self.graph.neighbors(node):
            if (
                self.node_colors[neighbor] == _NodeColor.UNVISITED
                and self.edge_types.get((node, neighbor)) == EdgeType.TREE
            ):
                self._animate_subtree(neighbor)

        self.node_colors[node] = _NodeColor.FINISHED
        self._record_time(node, is_discovery=False)
        self._draw(
            f"Finished node {node}  "
            f"(d={self.current_d_times[node]}, f={self.current_f_times[node]})"
        )

    def _record_time(self, node: int, *, is_discovery: bool) -> None:
        self._current_time += 1
        target = self.current_d_times if is_discovery else self.current_f_times
        target[node] = self._current_time

    def _draw(self, title: str = "") -> None:
        plt.clf()
        ax = plt.gca()

        edge_labels = {(u, v): self.edge_types.get((u, v), "") for u, v in self.graph.edges()}

        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            font_weight="bold",
            node_size=700,
            node_color=self.node_colors,
            arrows=True,
            ax=ax,
        )
        nx.draw_networkx_edge_labels(
            self.graph, self.pos, edge_labels=edge_labels, font_size=8, ax=ax
        )

        d_text = "d: " + ", ".join(
            f"{i}:{t}" for i, t in enumerate(self.current_d_times) if t > 0
        )
        f_text = "f: " + ", ".join(
            f"{i}:{t}" for i, t in enumerate(self.current_f_times) if t > 0
        )
        ax.text(
            0.01, 0.98, f"{d_text}\n{f_text}",
            transform=ax.transAxes,
            verticalalignment="top",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8),
        )

        plt.title(title)
        plt.pause(self.pause_duration)

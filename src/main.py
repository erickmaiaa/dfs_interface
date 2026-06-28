import argparse
import logging
import sys

from src.graph.builder import build_graph_from_file
from src.algorithms.dfs import perform_dfs
from src.visualization.animator import DfsVisualizer

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Perform and animate Depth-First Search on a directed graph."
    )
    parser.add_argument(
        "file_path",
        nargs="?",
        default="./data/G1.txt",
        help="Path to the graph file (default: ./data/G1.txt).",
    )
    parser.add_argument(
        "-p", "--pause",
        type=float,
        default=1.0,
        help="Pause duration in seconds between animation steps (default: 1.0).",
    )
    args = parser.parse_args()

    try:
        data = build_graph_from_file(args.file_path)
    except (FileNotFoundError, ValueError) as exc:
        log.error("Failed to load graph: %s", exc)
        sys.exit(1)

    log.info(
        "Graph loaded: %d vertices, %d edges.",
        data.num_vertices,
        data.graph.number_of_edges(),
    )
    log.info("DFS start vertex (highest outdegree): %d", data.start_node)

    edge_types, d_times, f_times = perform_dfs(
        data.adj_list, data.vertices_by_outdegree, data.num_vertices
    )

    log.info("DFS complete.")
    log.info("Discovery times (d): %s", d_times)
    log.info("Finish times    (f): %s", f_times)

    log.info("Starting animation...")
    visualizer = DfsVisualizer(
        data.graph, data.start_node, edge_types, d_times, f_times,
        pause_duration=args.pause,
    )
    visualizer.run_animation()


if __name__ == "__main__":
    main()

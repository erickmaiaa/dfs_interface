import argparse
from src.graph.builder import build_graph_from_file
from src.algorithms.dfs import perform_dfs
from src.visualization.animator import DfsVisualizer


def main():
    parser = argparse.ArgumentParser(
        description="Perform and animate Depth First Search on a graph from a file.")
    parser.add_argument("file_path", nargs='?', default='./data/G1.txt',
                        help="Path to the graph file (default: ./data/G1.txt).")
    parser.add_argument("-p", "--pause", type=float, default=1.0,
                        help="Pause duration in seconds between animation steps.")
    args = parser.parse_args()

    try:
        graph, start_node_for_anim, num_vertices, adj_list, vertices_by_degree = build_graph_from_file(
            args.file_path)

        print(
            f"Graph built: {num_vertices} vertices, {graph.number_of_edges()} edges.")
        print(
            f"Highest degree vertex (for animation start): {start_node_for_anim}")

        edge_types, d_times, f_times = perform_dfs(
            adj_list, vertices_by_degree, num_vertices)

        print("DFS complete. Calculated edge types, discovery and finish times.")
        print(f"Discovery Times (d): {d_times}")
        print(f"Finish Times (f): {f_times}")

        print("Starting animation...")
        visualizer = DfsVisualizer(
            graph, start_node_for_anim, edge_types, d_times, f_times, pause_duration=args.pause)
        visualizer.run_animation()

    except (FileNotFoundError, ValueError, SystemExit) as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

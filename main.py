from src.graph_builder import build_graph
from src.graph_animator import dfs_animation
from src.graph_dfs import dfs_graph

def main():
    file_path = './data/G1.txt'

    graph, high_degree_vertex, N_VERTEX, adj_list, HIGH_DEGREE_VERTEX_ADJ = build_graph(file_path)

    edge_types, d, f  = dfs_graph(adj_list, HIGH_DEGREE_VERTEX_ADJ, N_VERTEX)

    dfs_animation(graph, high_degree_vertex, edge_types, d, f)

if __name__ == "__main__":
    main()
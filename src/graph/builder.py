import networkx as nx
from collections import Counter


def build_graph_from_file(file_path):
    try:
        with open(file_path, "r") as graph_file:
            lines = graph_file.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        raise

    if not lines:
        raise ValueError("Graph file is empty.")

    try:
        parts = lines[0].split()
        if len(parts) < 2:
            raise ValueError(
                "First line must contain at least num_vertices and num_edges.")
        num_vertices, num_edges = map(int, parts[:2])
    except (ValueError, IndexError):
        raise ValueError(
            "Invalid first line format. Expected at least: num_vertices num_edges")

    if num_vertices <= 0:
        print("Error: Graph must have at least one vertex.")
        exit()

    adj_list = [[] for _ in range(num_vertices)]
    edges = []
    source_vertices = []

    if len(lines) < num_edges + 1:
        print(
            f"Warning: File contains fewer lines ({len(lines)-1}) than expected edges ({num_edges}). Processing available lines.")
        num_edges = len(lines) - 1

    if num_edges > 0:
        for i in range(1, num_edges + 1):
            try:
                line_content = lines[i].split()
                if len(line_content) < 2:
                    raise ValueError(
                        f"Invalid edge format in line {i+1}. Expected: source_vertex target_vertex")
                u, v = map(int, line_content[:2])
                if not (0 <= u < num_vertices and 0 <= v < num_vertices):
                    raise ValueError(
                        f"Vertex index out of range [0, {num_vertices-1}] in edge on line {i+1}: {u} {v}")
                edges.append((u, v))
                adj_list[u].append(v)
                source_vertices.append(u)
            except ValueError as e:
                raise ValueError(
                    f"Invalid data on line {i+1}: {lines[i].strip()}. Original error: {e}")

    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_vertices))
    graph.add_edges_from(edges)

    if not source_vertices:
        highest_degree_vertex = 0
        vertices_sorted_by_degree = list(range(num_vertices))
    else:
        degree_counts = Counter(source_vertices)
        vertices_sorted_by_degree_tuples = degree_counts.most_common()
        highest_degree_vertex = vertices_sorted_by_degree_tuples[
            0][0] if vertices_sorted_by_degree_tuples else 0
        vertices_sorted_by_degree = [
            v for v, _ in vertices_sorted_by_degree_tuples]
        all_vertices = set(range(num_vertices))
        vertices_with_degree = set(vertices_sorted_by_degree)
        vertices_sorted_by_degree.extend(
            sorted(list(all_vertices - vertices_with_degree)))

    return graph, highest_degree_vertex, num_vertices, adj_list, vertices_sorted_by_degree

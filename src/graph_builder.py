from collections import Counter
import networkx as nx

def build_graph(file_path):

    with open(file_path, "r") as graph_file:
        graph = graph_file.readlines()

    N_VERTEX = int(graph[0].split()[0])
    N_EDGES = int(graph[0].split()[1])
    HIGH_DEGREE_VERTEX = 0

    exit_degrees = []
    left_column = []
    right_column = []
    adj_list = [[] for _ in range(N_VERTEX)]

    if N_EDGES > 0:

        for i in range(1, N_EDGES + 1):
            left_column.append(int(graph[i].split()[0]))
            right_column.append(int(graph[i].split()[1]))

        for line in graph[1:]:
            vertex1, vertex2 = line.split()
            vertex1, vertex2 = int(vertex1), int(vertex2)
            exit_degrees.append(vertex1)
            adj_list[vertex1].append(vertex2)
        
        count_degrees = Counter(exit_degrees)
        most_count_degree = count_degrees.most_common()
        HIGH_DEGREE_VERTEX_ADJ = [element for element, _ in most_count_degree]
        most_count_degree = most_count_degree[0][0]
        HIGH_DEGREE_VERTEX = most_count_degree
        

    G = nx.DiGraph()

    if N_VERTEX > 0:
        for i in range(N_VERTEX):
            if i not in G.nodes():
                G.add_node(i)
    else:
        print("No vertex found")
        exit()

    if N_EDGES > 0:
        for i in range(len(left_column)):
            G.add_edge(int(left_column[i]), int(right_column[i]))

    return G, HIGH_DEGREE_VERTEX, N_VERTEX, adj_list, HIGH_DEGREE_VERTEX_ADJ


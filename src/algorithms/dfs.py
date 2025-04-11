def perform_dfs(adj_list, start_vertices, num_vertices):
    discovery_times = [0] * num_vertices
    finish_times = [0] * num_vertices
    vertex_colors = ["white"] * num_vertices
    edge_types = {}
    time_stamp = 0

    EDGE_TYPE_TREE = "Tree"
    EDGE_TYPE_BACK = "Back"
    EDGE_TYPE_FORWARD = "Forward"
    EDGE_TYPE_CROSS = "Cross"

    def dfs_visit(u):
        nonlocal time_stamp
        vertex_colors[u] = "gray"
        time_stamp += 1
        discovery_times[u] = time_stamp

        for v in adj_list[u]:
            edge = (u, v)
            if vertex_colors[v] == "white":
                edge_types[edge] = EDGE_TYPE_TREE
                dfs_visit(v)
            elif vertex_colors[v] == "gray":
                edge_types[edge] = EDGE_TYPE_BACK
            else:
                if discovery_times[u] < discovery_times[v]:
                    edge_types[edge] = EDGE_TYPE_FORWARD
                else:
                    edge_types[edge] = EDGE_TYPE_CROSS

        vertex_colors[u] = "black"
        time_stamp += 1
        finish_times[u] = time_stamp

    for u in start_vertices:
        if vertex_colors[u] == "white":
            dfs_visit(u)

    for u in range(num_vertices):
        if vertex_colors[u] == "white":
            dfs_visit(u)

    return edge_types, discovery_times, finish_times

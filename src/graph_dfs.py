def dfs_graph(adj_list, high_degree, N):

    d, f = [0] * N, [0] * N
    color = ["white"] * N
    edge_types, mark = {}, 0
    
    def dfs_visit(u):
        nonlocal mark  # Use nonlocal instead of global
        color[u] = "gray"
        mark += 1
        d[u] = mark

        for v in adj_list[u]:
            if color[v] == "white":
                edge_types[(u, v)] = "Arvore"
                dfs_visit(v)
            elif color[v] == "gray":
                edge_types[(u, v)] = "Retorno"
            else:
                if d[u] < d[v]:
                    edge_types[(u, v)] = "Avanco"
                else:
                    edge_types[(u, v)] = "Cruzamento"
        color[u] = "black"
        mark += 1
        f[u] = mark


    def dfs():
        for u in high_degree:
            if color[u] == "white":
                dfs_visit(u)
    
    dfs()

    return edge_types, d, f

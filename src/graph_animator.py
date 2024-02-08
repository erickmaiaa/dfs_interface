import matplotlib.pyplot as plt
import networkx as nx
from time import sleep

def dfs_animation(G, start_node, edge_types, d, f):
    pos = nx.spring_layout(G) if G.number_of_nodes() > 0 else {}
    node_colors = ['lightgray'] * G.number_of_nodes()

    pre_order = {start_node: 1}
    post_order = {}
    order = []

    def get_edge_label(u, v):
        edge_key = (u, v)
        if edge_key in edge_types:
            return edge_types[edge_key]
        elif (v, u) in edge_types:
            return edge_types[(v, u)]
        else:
            return 'No Label'

    def display_values():
        plt.text(0, 1, f'vetor d: {d}\nvetor f: {f}', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    display_values() 

    def dfs(node):
        nonlocal order
        order.append(node)
        node_colors[node] = 'gray'
        edge_labels = {(u, v): get_edge_label(u, v) for u, v in G.edges()}
        
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color=node_colors, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        nx.draw_networkx_labels(G, pos, font_color='white')

        plt.pause(5)

        for neighbor in G.neighbors(node):
            if neighbor not in pre_order:
                pre_order[neighbor] = len(pre_order) + 1
                dfs(neighbor)

        post_order[node] = len(post_order) + 1
        node_colors[node] = 'black'
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color=node_colors, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        nx.draw_networkx_labels(G, pos, font_color='white')

        plt.pause(5)

    dfs(start_node)

    plt.show()


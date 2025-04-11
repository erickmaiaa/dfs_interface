import matplotlib.pyplot as plt
import networkx as nx


class DfsVisualizer:

    def __init__(self, graph, start_node, edge_types, d_times, f_times, pause_duration=1.0):
        self.graph = graph
        self.start_node = start_node
        self.edge_types = edge_types
        self.d_times = d_times
        self.f_times = f_times
        self.pause_duration = pause_duration

        self.pos = nx.spring_layout(
            self.graph) if self.graph.number_of_nodes() > 0 else {}
        self.node_colors = ['lightgray'] * self.graph.number_of_nodes()
        self.visited_order = []
        self.current_time = 0
        self.current_d_times = [0] * self.graph.number_of_nodes()
        self.current_f_times = [0] * self.graph.number_of_nodes()

        plt.figure(figsize=(10, 8))
        self._draw_graph_state("Initial State")

    def _get_edge_label(self, u, v):
        return self.edge_types.get((u, v), '')

    def _update_time_vectors(self, node, is_discovery):
        if is_discovery:
            self.current_time += 1
            self.current_d_times[node] = self.current_time
        else:
            self.current_time += 1
            self.current_f_times[node] = self.current_time

    def _draw_graph_state(self, title=""):
        plt.clf()
        ax = plt.gca()

        edge_labels = {(u, v): self._get_edge_label(u, v)
                       for u, v in self.graph.edges()}

        nx.draw(self.graph, self.pos, with_labels=True, font_weight='bold',
                node_size=700, node_color=self.node_colors, arrows=True, ax=ax)
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels,
                                     font_size=8, ax=ax)

        label_pos = {k: (v[0], v[1] + 0.05) for k, v in self.pos.items()}
        nx.draw_networkx_labels(self.graph, label_pos,
                                font_color='black', font_weight='bold', ax=ax)

        d_text = "d: " + \
            ", ".join(f"{i}:{t}" for i, t in enumerate(
                self.current_d_times) if t > 0)
        f_text = "f: " + \
            ", ".join(f"{i}:{t}" for i, t in enumerate(
                self.current_f_times) if t > 0)
        plt.text(0.01, 0.98, f"{d_text}\n{f_text}", transform=ax.transAxes,
                 verticalalignment='top', fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))

        plt.title(title)
        plt.pause(self.pause_duration)

    def _animate_step(self, node):
        self.visited_order.append(node)
        self.node_colors[node] = 'gray'
        self._update_time_vectors(node, is_discovery=True)
        self._draw_graph_state(
            f"Visiting node {node} (d={self.current_d_times[node]})")

        for neighbor in self.graph.neighbors(node):
            if self.node_colors[neighbor] == 'lightgray':
                if (node, neighbor) in self.edge_types and self.edge_types[(node, neighbor)] == "Tree":
                    self._animate_step(neighbor)

        self.node_colors[node] = 'black'
        self._update_time_vectors(node, is_discovery=False)
        self._draw_graph_state(
            f"Finished node {node} (d={self.current_d_times[node]}, f={self.current_f_times[node]})")

    def run_animation(self):
        if self.start_node is not None and 0 <= self.start_node < self.graph.number_of_nodes():
            if self.node_colors[self.start_node] == 'lightgray':
                self._animate_step(self.start_node)
        else:
            print(
                f"Warning: Invalid start node ({self.start_node}). No animation shown.")

        self._draw_graph_state("DFS Complete")
        plt.show()

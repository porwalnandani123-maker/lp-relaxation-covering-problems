"""
graphs.py
Generates graph instances for the Vertex Cover / Set Cover experiments.

Graph families:
- Random G(n, p)
- Bipartite
- Complete
"""

import networkx as nx


def random_graph(n: int, p: float, seed: int = None) -> nx.Graph:
    """Generate a random graph using the Erdos-Renyi model."""
    return nx.erdos_renyi_graph(n, p, seed=seed)


def bipartite_graph(n1: int, n2: int, p: float, seed: int = None) -> nx.Graph:
    """Generate a random bipartite graph with two node sets of size n1 and n2."""
    return nx.bipartite.random_graph(n1, n2, p, seed=seed)


def complete_graph(n: int) -> nx.Graph:
    """Generate a complete graph on n vertices."""
    return nx.complete_graph(n)


if __name__ == "__main__":
    # Quick sanity check when running this file directly
    g1 = random_graph(10, 0.3, seed=42)
    g2 = bipartite_graph(5, 5, 0.3, seed=42)
    g3 = complete_graph(6)

    print(f"Random graph: {g1.number_of_nodes()} nodes, {g1.number_of_edges()} edges")
    print(f"Bipartite graph: {g2.number_of_nodes()} nodes, {g2.number_of_edges()} edges")
    print(f"Complete graph: {g3.number_of_nodes()} nodes, {g3.number_of_edges()} edges")
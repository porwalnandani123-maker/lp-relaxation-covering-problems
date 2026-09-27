"""
exact.py
Exact solvers for Vertex Cover, used as ground truth on small graphs.
Brute-force: fine for n <= ~20.
"""

import itertools
import networkx as nx


def exact_vertex_cover(G: nx.Graph) -> set:
    """
    Find the minimum vertex cover by brute-force search over subset sizes.
    Only practical for small graphs (n <= ~20).
    """
    nodes = list(G.nodes())
    edges = list(G.edges())

    # Try increasing subset sizes until we find a valid cover
    for size in range(len(nodes) + 1):
        for subset in itertools.combinations(nodes, size):
            subset_set = set(subset)
            if all(u in subset_set or v in subset_set for u, v in edges):
                return subset_set

    return set(nodes)  # fallback: shouldn't be reached


if __name__ == "__main__":
    from graphs import random_graph, bipartite_graph, complete_graph

    g1 = random_graph(8, 0.4, seed=1)
    cover = exact_vertex_cover(g1)
    print(f"Random graph (8 nodes): minimum vertex cover size = {len(cover)}")
    print(f"Cover: {cover}")

    g2 = complete_graph(5)
    cover2 = exact_vertex_cover(g2)
    print(f"Complete graph (5 nodes): minimum vertex cover size = {len(cover2)}")
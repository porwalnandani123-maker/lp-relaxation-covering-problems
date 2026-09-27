"""
heuristics.py
Simple combinatorial heuristics for Vertex Cover:
- Greedy (highest-degree vertex first)
- Maximal matching
"""

import networkx as nx


def greedy_vertex_cover(G: nx.Graph) -> set:
    """Repeatedly pick the highest-degree vertex, remove it, repeat."""
    G = G.copy()
    cover = set()

    while G.number_of_edges() > 0:
        # Pick vertex with max degree
        v = max(G.nodes(), key=lambda x: G.degree(x))
        cover.add(v)
        G.remove_node(v)

    return cover


def matching_vertex_cover(G: nx.Graph) -> set:
    """Take both endpoints of every edge in a maximal matching."""
    matching = nx.maximal_matching(G)
    cover = set()
    for u, v in matching:
        cover.add(u)
        cover.add(v)
    return cover


if __name__ == "__main__":
    from graphs import random_graph, complete_graph
    from exact import exact_vertex_cover

    g = random_graph(8, 0.4, seed=1)

    exact = exact_vertex_cover(g)
    greedy = greedy_vertex_cover(g)
    matching = matching_vertex_cover(g)

    print(f"Exact cover size: {len(exact)}")
    print(f"Greedy cover size: {len(greedy)}")
    print(f"Matching cover size: {len(matching)}")
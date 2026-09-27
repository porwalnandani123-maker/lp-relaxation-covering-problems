"""
primal_dual.py
Primal-dual algorithm for Vertex Cover.
Raises a "price" on each uncovered edge until some vertex is fully paid for,
then adds that vertex to the cover.
"""

import networkx as nx


def primal_dual_vertex_cover(G: nx.Graph) -> set:
    """
    Primal-dual 2-approximation for Vertex Cover.
    Each vertex has a budget of 0. We raise dual variables y_e for
    uncovered edges until some vertex's total incoming payment reaches 1
    (its cost), then add it to the cover and remove its edges.
    """
    G = G.copy()
    cover = set()
    y = {}  # dual variable per edge

    remaining_edges = list(G.edges())

    while remaining_edges:
        # Track how much each vertex has been "paid" so far
        paid = {v: 0.0 for v in G.nodes()}
        for (u, v), val in y.items():
            if u in paid:
                paid[u] += val
            if v in paid:
                paid[v] += val

        # Raise y_e uniformly for all remaining edges until some vertex hits 1
        # Find the tightest edge: the one closest to saturating a vertex
        slack = []
        for (u, v) in remaining_edges:
            slack.append((1 - paid[u], u, v))
            slack.append((1 - paid[v], v, u))

        delta = min(s for s, _, _ in slack)
        delta = max(delta, 0)

        for (u, v) in remaining_edges:
            y[(u, v)] = y.get((u, v), 0.0) + delta
            paid[u] += delta
            paid[v] += delta

        # Add any vertex that reached its budget of 1
        newly_covered = [v for v in G.nodes() if paid[v] >= 1 - 1e-9 and v not in cover]
        for v in newly_covered:
            cover.add(v)

        # Remove edges covered by the new vertices
        remaining_edges = [(u, v) for (u, v) in remaining_edges
                           if u not in cover and v not in cover]

    return cover


if __name__ == "__main__":
    from graphs import random_graph, complete_graph
    from exact import exact_vertex_cover

    for name, g in [
        ("Random", random_graph(8, 0.4, seed=1)),
        ("Complete", complete_graph(5)),
    ]:
        exact = exact_vertex_cover(g)
        pd_cover = primal_dual_vertex_cover(g)

        print(f"{name} graph: exact = {len(exact)}, primal-dual = {len(pd_cover)}")
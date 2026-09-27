"""
nemhauser_trotter.py
Nemhauser-Trotter preprocessing for Vertex Cover.

Uses the LP relaxation solution to fix vertices at 0 or 1,
and shrinks the graph to only the vertices with LP value exactly 0.5.

Theorem (informal): there always exists an optimal vertex cover that
includes every vertex with LP value 1, and excludes every vertex with
LP value 0. Only the 0.5-valued vertices are genuinely undecided.
"""

import networkx as nx
from lp_rounding import lp_relaxation_vertex_cover


def nemhauser_trotter_reduce(G: nx.Graph, tol: float = 1e-6):
    """
    Reduce G using its LP relaxation solution.

    Returns:
        forced_in: set of vertices forced into every optimal cover (LP value 1)
        forced_out: set of vertices forced out of every optimal cover (LP value 0)
        reduced_graph: subgraph induced on the remaining ("undecided", LP value 0.5) vertices
    """
    lp_vals = lp_relaxation_vertex_cover(G)

    forced_in = {v for v, val in lp_vals.items() if val > 1 - tol}
    forced_out = {v for v, val in lp_vals.items() if val < tol}
    undecided = {v for v, val in lp_vals.items()
                 if tol <= val <= 1 - tol}

    reduced_graph = G.subgraph(undecided).copy()

    return forced_in, forced_out, reduced_graph


if __name__ == "__main__":
    from graphs import random_graph, complete_graph

    for name, g in [
        ("Random", random_graph(20, 0.3, seed=7)),
        ("Complete", complete_graph(10)),
    ]:
        forced_in, forced_out, reduced = nemhauser_trotter_reduce(g)

        print(f"\n{name} graph:")
        print(f"  Original: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")
        print(f"  Forced IN (LP=1): {len(forced_in)} vertices")
        print(f"  Forced OUT (LP=0): {len(forced_out)} vertices")
        print(f"  Reduced (undecided, LP=0.5): {reduced.number_of_nodes()} nodes, "
              f"{reduced.number_of_edges()} edges")
        reduction_pct = 100 * (1 - reduced.number_of_nodes() / g.number_of_nodes())
        print(f"  Size reduction: {reduction_pct:.1f}%")

        print("\n--- Testing sparser random graphs ---")
    for p in [0.05, 0.1, 0.15, 0.2]:
        g = random_graph(30, p, seed=7)
        forced_in, forced_out, reduced = nemhauser_trotter_reduce(g)
        reduction_pct = 100 * (1 - reduced.number_of_nodes() / g.number_of_nodes())
        print(f"p={p}: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges -> "
              f"reduction {reduction_pct:.1f}% ({len(forced_in)} in, {len(forced_out)} out)")

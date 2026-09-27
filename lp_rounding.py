"""
lp_rounding.py
LP relaxation and rounding for Vertex Cover.
Also checks half-integrality of the LP solution.
"""

import numpy as np
from scipy.optimize import linprog
import networkx as nx


def lp_relaxation_vertex_cover(G: nx.Graph):
    """
    Solve the LP relaxation of Vertex Cover.
    Returns the fractional solution as a dict {node: value}.
    """
    nodes = list(G.nodes())
    n = len(nodes)
    node_index = {v: i for i, v in enumerate(nodes)}
    edges = list(G.edges())

    # Objective: minimize sum of x_v
    c = np.ones(n)

    # Constraints: x_u + x_v >= 1 for each edge -> -x_u - x_v <= -1
    A_ub = []
    b_ub = []
    for u, v in edges:
        row = np.zeros(n)
        row[node_index[u]] = -1
        row[node_index[v]] = -1
        A_ub.append(row)
        b_ub.append(-1)

    bounds = [(0, 1) for _ in range(n)]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not result.success:
        raise RuntimeError("LP did not solve successfully")

    return {nodes[i]: result.x[i] for i in range(n)}


def round_lp_solution(lp_values: dict, threshold: float = 0.5) -> set:
    """Round: include any vertex whose LP value is >= threshold."""
    return {v for v, val in lp_values.items() if val >= threshold - 1e-9}


def check_half_integrality(lp_values: dict, tol: float = 1e-6) -> bool:
    """Check that every LP value is (close to) 0, 0.5, or 1."""
    for val in lp_values.values():
        if not (abs(val - 0) < tol or abs(val - 0.5) < tol or abs(val - 1) < tol):
            return False
    return True


if __name__ == "__main__":
    from graphs import random_graph, bipartite_graph, complete_graph
    from exact import exact_vertex_cover

    for name, g in [
        ("Random", random_graph(8, 0.4, seed=1)),
        ("Bipartite", bipartite_graph(4, 4, 0.4, seed=1)),
        ("Complete", complete_graph(5)),
    ]:
        lp_vals = lp_relaxation_vertex_cover(g)
        rounded = round_lp_solution(lp_vals)
        exact = exact_vertex_cover(g)
        half_int = check_half_integrality(lp_vals)

        lp_optimum = sum(lp_vals.values())
        exact_optimum = len(exact)
        gap = lp_optimum / exact_optimum if exact_optimum > 0 else 1.0

        print(f"\n{name} graph:")
        print(f"  LP values: { {k: round(v,2) for k,v in lp_vals.items()} }")
        print(f"  Half-integral: {half_int}")
        print(f"  LP optimum: {lp_optimum:.2f}, Exact optimum: {exact_optimum}")
        print(f"  Integrality gap: {gap:.3f}")
        print(f"  Rounded cover size: {len(rounded)}")
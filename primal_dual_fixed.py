"""
primal_dual_fixed.py

Corrected primal-dual algorithms for Vertex Cover and Set Cover (unit costs).

Why this file exists
--------------------
The original primal_dual.py / set_cover_primal_dual.py raise every uncovered
dual variable by the same `delta`, where delta = min over sets/vertices of
(1 - paid). But a set S with k uncovered elements receives k * delta of payment
per round, not delta, so its dual constraint  sum_{e in S} y_e <= 1  can be
overshot. Once the dual is infeasible, the guarantee  |cover| <= f * OPT  no
longer holds (the original code returned 2.67x OPT on a 10-node random graph).

Fix: step size = min over sets of (1 - paid_S) / |S & uncovered|.
This keeps y dual-feasible, and every chosen set is exactly tight, so

    |cover| = sum_{S chosen} sum_{e in S} y_e  <=  f * sum_e y_e  <=  f * LP <= f * OPT.
"""


def primal_dual_set_cover_fixed(universe, subsets, return_dual=False):
    uncovered = set(universe)
    y = {e: 0.0 for e in universe}
    paid = [0.0] * len(subsets)
    chosen = []
    chosen_set = set()
    while uncovered:
        best_delta = None
        for i, s in enumerate(subsets):
            if i in chosen_set:
                continue
            k = len(s & uncovered)
            if k == 0:
                continue
            d = (1.0 - paid[i]) / k
            if best_delta is None or d < best_delta:
                best_delta = d
        if best_delta is None:
            break  # infeasible instance
        best_delta = max(best_delta, 0.0)
        for e in uncovered:
            y[e] += best_delta
        for i, s in enumerate(subsets):
            if i in chosen_set:
                continue
            paid[i] += best_delta * len(s & uncovered)
        newly = [i for i, s in enumerate(subsets)
                 if i not in chosen_set and (s & uncovered) and paid[i] >= 1 - 1e-9]
        for i in newly:
            chosen.append(i)
            chosen_set.add(i)
        for i in newly:
            uncovered -= subsets[i]
    if return_dual:
        return chosen, y
    return chosen


def primal_dual_vertex_cover_fixed(G):
    """Vertex Cover as the f=2 special case: elements = edges, sets = vertices."""
    nodes = list(G.nodes())
    edges = list(G.edges())
    eid = {}
    for i, (u, v) in enumerate(edges):
        eid[(u, v)] = i
        eid[(v, u)] = i
    subsets = [set() for _ in nodes]
    pos = {v: i for i, v in enumerate(nodes)}
    for (u, v), i in ((e, eid[e]) for e in edges):
        subsets[pos[u]].add(i)
        subsets[pos[v]].add(i)
    chosen = primal_dual_set_cover_fixed(list(range(len(edges))), subsets)
    return {nodes[i] for i in chosen}
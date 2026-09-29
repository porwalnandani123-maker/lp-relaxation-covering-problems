"""Exact solvers via scipy.optimize.milp (scales far beyond brute force)."""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def exact_set_cover_milp(universe, subsets, forced_in=(), forced_out=()):
    """Return the minimum number of subsets covering `universe` (int),
    with optional forced_in / forced_out subset indices. None if infeasible."""
    m = len(subsets)
    elems = list(universe)
    if not elems:
        return len(set(forced_in))
    A = np.zeros((len(elems), m))
    pos = {e: r for r, e in enumerate(elems)}
    for j, s in enumerate(subsets):
        for e in s:
            if e in pos:
                A[pos[e], j] = 1
    lb = np.zeros(m)
    ub = np.ones(m)
    for j in forced_in:
        lb[j] = 1
    for j in forced_out:
        ub[j] = 0
    res = milp(np.ones(m), constraints=LinearConstraint(A, lb=1),
               integrality=np.ones(m), bounds=Bounds(lb, ub))
    if not res.success:
        return None
    return int(round(res.fun))


def exact_vertex_cover_milp(G):
    nodes = list(G.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    edges = list(G.edges())
    if not edges:
        return 0
    A = np.zeros((len(edges), len(nodes)))
    for r, (u, v) in enumerate(edges):
        A[r, idx[u]] = 1
        A[r, idx[v]] = 1
    res = milp(np.ones(len(nodes)), constraints=LinearConstraint(A, lb=1),
               integrality=np.ones(len(nodes)), bounds=Bounds(0, 1))
    return int(round(res.fun))
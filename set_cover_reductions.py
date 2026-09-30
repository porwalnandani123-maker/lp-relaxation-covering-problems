"""
set_cover_reductions.py

Preprocessing for (unit-cost) Set Cover -- the Set Cover analogue of
Nemhauser-Trotter for Vertex Cover.

Two families are implemented and kept deliberately separate, because they have
different guarantees:

1. SAFE combinatorial rules (exact: they never increase the optimum)
     R1 essential set : an element in exactly one set forces that set in.
     R2 dominated set : a set contained in another set can be dropped.
     R3 dominated elem: if every set covering e' also covers e, drop e.
   Applied to a fixpoint by `reduce_instance`.

2. LP-based fixing (`lp_fixing`), the direct NT analogue: fix x_S=1 -> in,
   x_S=0 -> out. Nemhauser-Trotter proves this is safe for Vertex Cover
   because its LP is half-integral. Set Cover's LP has no such property, so
   LP fixing is only a HEURISTIC here; `persistency_holds` tests empirically
   whether the fixed choices are consistent with some optimal cover.
"""
import numpy as np
from set_cover_lp import lp_relaxation_set_cover
from exact_milp import exact_set_cover_milp


def reduce_instance(universe, subsets):
    """Apply R1-R3 to a fixpoint.
    Returns (forced, red_universe, red_subsets, index_map) where `forced` are
    ORIGINAL indices of sets that must be in the cover, `red_subsets[k]` is the
    restricted set for original index index_map[k]."""
    E = set(universe)
    A = {i: set(s) & E for i, s in enumerate(subsets)}
    forced = []
    changed = True
    while changed and E:
        changed = False
        # R1: essential sets
        cover_of = {e: [] for e in E}
        for i, s in A.items():
            for e in s:
                cover_of[e].append(i)
        for e in list(E):
            if e in E and len(cover_of[e]) == 1:
                i = cover_of[e][0]
                if i in A:
                    forced.append(i)
                    E -= A[i]
                    del A[i]
                    A = {j: (s & E) for j, s in A.items()}
                    changed = True
                    cover_of = {x: [] for x in E}
                    for j, s in A.items():
                        for x in s:
                            cover_of[x].append(j)
        A = {i: s for i, s in A.items() if s}          # drop empty sets
        # R2: dominated sets (ties broken by index)
        keys = sorted(A)
        for i in keys:
            if i not in A:
                continue
            for j in keys:
                if j == i or j not in A:
                    continue
                if A[i] <= A[j] and (A[i] != A[j] or j < i):
                    del A[i]
                    changed = True
                    break
        # R3: dominated elements
        cover_of = {e: frozenset(i for i, s in A.items() if e in s) for e in E}
        elems = sorted(E)
        for e in elems:
            if e not in E:
                continue
            for e2 in elems:
                if e2 == e or e2 not in E:
                    continue
                if cover_of[e2] <= cover_of[e] and (cover_of[e2] != cover_of[e] or e2 < e):
                    E.discard(e)          # covering e2 automatically covers e
                    changed = True
                    break
        A = {i: (s & E) for i, s in A.items()}
        A = {i: s for i, s in A.items() if s}
    index_map = sorted(A)
    return forced, sorted(E), [A[i] for i in index_map], index_map


def solve_with_reduction(universe, subsets, algo):
    """Run algo(universe, subsets)->indices on the reduced instance and map back.
    Returns the list of ORIGINAL subset indices forming a valid cover."""
    forced, ru, rs, imap = reduce_instance(universe, subsets)
    sol = list(forced)
    if ru:
        sol += [imap[k] for k in algo(ru, rs)]
    return sol


def lp_fixing(universe, subsets, tol=1e-6):
    x = lp_relaxation_set_cover(universe, subsets)
    fin = [i for i, v in enumerate(x) if v > 1 - tol]
    fout = [i for i, v in enumerate(x) if v < tol]
    return x, fin, fout


def persistency_holds(universe, subsets, forced_in, forced_out, opt=None):
    """True iff some optimal cover contains all forced_in and none of forced_out."""
    if opt is None:
        opt = exact_set_cover_milp(universe, subsets)
    val = exact_set_cover_milp(universe, subsets, forced_in=forced_in, forced_out=forced_out)
    return val is not None and val == opt
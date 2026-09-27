"""
set_cover_lp.py
LP relaxation and rounding for Set Cover.
Rounding threshold is 1/f, where f = max frequency of any element
across all subsets (this gives an f-approximation, generalizing
Vertex Cover's 2-approximation, since f=2 there).
"""

import numpy as np
from scipy.optimize import linprog


def compute_max_frequency(universe, subsets):
    """f = the largest number of subsets containing any single element."""
    freq = {elem: 0 for elem in universe}
    for s in subsets:
        for elem in s:
            freq[elem] += 1
    return max(freq.values()) if freq else 1


def lp_relaxation_set_cover(universe, subsets):
    """
    Solve the LP relaxation of Set Cover.
    Variable x_i in [0,1] for each subset i.
    Constraint: for each element, sum of x_i over subsets containing it >= 1.
    Returns the fractional solution as a list of values, one per subset.
    """
    num_subsets = len(subsets)
    c = np.ones(num_subsets)  # minimize sum of x_i

    A_ub = []
    b_ub = []
    for elem in universe:
        row = np.zeros(num_subsets)
        for i, s in enumerate(subsets):
            if elem in s:
                row[i] = -1  # negate since linprog does <=, we need >=
        A_ub.append(row)
        b_ub.append(-1)

    bounds = [(0, 1) for _ in range(num_subsets)]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not result.success:
        raise RuntimeError("LP did not solve successfully")

    return result.x


def round_lp_set_cover(lp_values, universe, subsets):
    """Round up any subset whose LP value is >= 1/f."""
    f = compute_max_frequency(universe, subsets)
    threshold = 1.0 / f
    chosen = [i for i, val in enumerate(lp_values) if val >= threshold - 1e-9]
    return chosen


if __name__ == "__main__":
    from set_cover_instances import random_set_cover_instance
    from set_cover_exact import exact_set_cover
    from set_cover_heuristics import greedy_set_cover

    universe, subsets = random_set_cover_instance(10, 6, 5, seed=1)

    lp_vals = lp_relaxation_set_cover(universe, subsets)
    rounded = round_lp_set_cover(lp_vals, universe, subsets)
    f = compute_max_frequency(universe, subsets)

    exact = exact_set_cover(universe, subsets)
    greedy = greedy_set_cover(universe, subsets)

    print(f"Max frequency (f): {f}")
    print(f"LP values: {[round(v, 2) for v in lp_vals]}")
    print(f"LP optimum: {sum(lp_vals):.2f}")
    print(f"Rounded cover size: {len(rounded)} -> {rounded}")
    print(f"Exact cover size: {len(exact)} -> {exact}")
    print(f"Greedy cover size: {len(greedy)} -> {greedy}")
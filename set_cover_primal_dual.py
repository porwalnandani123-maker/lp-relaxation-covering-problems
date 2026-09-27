"""
set_cover_primal_dual.py
Primal-dual algorithm for Set Cover.
Raises a price on each uncovered element until some subset's total
incoming payment reaches its cost (1), then that subset is chosen.
"""


def primal_dual_set_cover(universe, subsets):
    """
    Primal-dual f-approximation for Set Cover (f = max element frequency).
    """
    uncovered = set(universe)
    chosen = []
    y = {elem: 0.0 for elem in universe}

    while uncovered:
        # For each subset, its "paid" amount is sum of y over its elements
        paid = []
        for s in subsets:
            paid.append(sum(y[e] for e in s))

        # Find the tightest subset: smallest remaining slack (1 - paid), among subsets
        # that still have at least one uncovered element
        candidates = [(1 - paid[i], i) for i, s in enumerate(subsets) if s & uncovered]
        if not candidates:
            break

        delta, tight_i = min(candidates)
        delta = max(delta, 0)

        # Raise y for all currently uncovered elements
        for e in uncovered:
            y[e] += delta

        # Recompute paid, pick any subset now fully paid (cost 1) with uncovered elements
        for i, s in enumerate(subsets):
            if i in chosen:
                continue
            paid_i = sum(y[e] for e in s)
            if paid_i >= 1 - 1e-9 and s & uncovered:
                chosen.append(i)
                uncovered -= s

    return chosen


if __name__ == "__main__":
    from set_cover_instances import random_set_cover_instance
    from set_cover_exact import exact_set_cover
    from set_cover_heuristics import greedy_set_cover
    from set_cover_lp import lp_relaxation_set_cover, round_lp_set_cover

    universe, subsets = random_set_cover_instance(10, 6, 5, seed=1)

    exact = exact_set_cover(universe, subsets)
    greedy = greedy_set_cover(universe, subsets)
    lp_vals = lp_relaxation_set_cover(universe, subsets)
    lp_rounded = round_lp_set_cover(lp_vals, universe, subsets)
    pd = primal_dual_set_cover(universe, subsets)

    print(f"Exact: {len(exact)} -> {exact}")
    print(f"Greedy: {len(greedy)} -> {greedy}")
    print(f"LP-rounding: {len(lp_rounded)} -> {lp_rounded}")
    print(f"Primal-dual: {len(pd)} -> {pd}")
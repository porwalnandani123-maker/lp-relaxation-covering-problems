"""
set_cover_exact.py
Exact solver for Set Cover, used as ground truth on small instances.
Brute-force: fine for a small number of subsets (~15-20 max).
"""

import itertools


def exact_set_cover(universe, subsets):
    """
    Find the minimum number of subsets that cover the entire universe.
    Brute-force: try increasing numbers of subsets until one combination covers everything.

    Returns a list of subset indices forming the minimum cover.
    """
    universe_set = set(universe)
    num_subsets = len(subsets)

    for size in range(1, num_subsets + 1):
        for combo in itertools.combinations(range(num_subsets), size):
            covered = set()
            for i in combo:
                covered |= subsets[i]
            if covered >= universe_set:
                return list(combo)

    return list(range(num_subsets))  # fallback: shouldn't be reached


if __name__ == "__main__":
    from set_cover_instances import random_set_cover_instance

    universe, subsets = random_set_cover_instance(10, 6, 5, seed=1)

    print(f"Universe size: {len(universe)}")
    print(f"Number of subsets: {len(subsets)}")
    for i, s in enumerate(subsets):
        print(f"  Set {i}: {sorted(s)}")

    cover = exact_set_cover(universe, subsets)
    print(f"\nMinimum set cover uses {len(cover)} subsets: {cover}")
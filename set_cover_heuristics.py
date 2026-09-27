"""
set_cover_heuristics.py
Greedy algorithm for Set Cover.
"""


def greedy_set_cover(universe, subsets):
    """
    Repeatedly pick the subset that covers the most currently-uncovered elements.
    Returns a list of subset indices forming the cover.
    """
    universe_set = set(universe)
    uncovered = set(universe_set)
    chosen = []
    remaining_subsets = list(enumerate(subsets))

    while uncovered:
        best_i, best_gain = None, -1
        for i, s in remaining_subsets:
            gain = len(s & uncovered)
            if gain > best_gain:
                best_gain = gain
                best_i = i

        if best_gain <= 0:
            break  # no subset covers any remaining element; shouldn't happen if instance is valid

        chosen.append(best_i)
        uncovered -= subsets[best_i]
        remaining_subsets = [(i, s) for i, s in remaining_subsets if i != best_i]

    return chosen


if __name__ == "__main__":
    from set_cover_instances import random_set_cover_instance
    from set_cover_exact import exact_set_cover

    universe, subsets = random_set_cover_instance(10, 6, 5, seed=1)

    exact = exact_set_cover(universe, subsets)
    greedy = greedy_set_cover(universe, subsets)

    print(f"Exact cover size: {len(exact)} -> {exact}")
    print(f"Greedy cover size: {len(greedy)} -> {greedy}")
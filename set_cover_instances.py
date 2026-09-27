"""
set_cover_instances.py
Generates Set Cover instances: a universe of elements and a collection of subsets.
"""

import random


def random_set_cover_instance(num_elements: int, num_sets: int, max_set_size: int, seed: int = None):
    """
    Generate a random Set Cover instance.
    Returns (universe, subsets) where universe is a list of element ids,
    and subsets is a list of sets, each a subset of the universe.
    Ensures every element is covered by at least one subset.
    """
    rng = random.Random(seed)
    universe = list(range(num_elements))

    subsets = []
    for _ in range(num_sets):
        size = rng.randint(1, max_set_size)
        subset = set(rng.sample(universe, min(size, num_elements)))
        subsets.append(subset)

    covered = set().union(*subsets) if subsets else set()
    missing = set(universe) - covered
    for elem in missing:
        subsets.append({elem})

    return universe, subsets


def vertex_cover_as_set_cover(G):
    """
    Convert a graph into a Set Cover instance: universe = edges,
    subsets = for each vertex, the set of edges incident to it.
    """
    edges = list(G.edges())
    universe = list(range(len(edges)))
    edge_index = {e: i for i, e in enumerate(edges)}
    edge_index.update({(v, u): i for (u, v), i in list(edge_index.items())})

    subsets = []
    for v in G.nodes():
        incident = {edge_index[e] for e in edges if v in e}
        subsets.append(incident)

    return universe, subsets


if __name__ == "__main__":
    universe, subsets = random_set_cover_instance(15, 8, 6, seed=1)
    print(f"Universe size: {len(universe)}")
    print(f"Number of subsets: {len(subsets)}")
    for i, s in enumerate(subsets):
        print(f"  Set {i}: {sorted(s)}")
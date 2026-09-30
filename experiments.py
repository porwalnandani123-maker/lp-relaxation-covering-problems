"""
experiments.py
Runs all Vertex Cover methods across graph families and sizes,
collects results, and plots approximation ratio vs. n.
"""

import matplotlib.pyplot as plt
from graphs import random_graph, bipartite_graph, complete_graph
from exact import exact_vertex_cover
from heuristics import greedy_vertex_cover, matching_vertex_cover
from lp_rounding import lp_relaxation_vertex_cover, round_lp_solution
from primal_dual_fixed import primal_dual_vertex_cover_fixed as primal_dual_vertex_cover


def run_all_methods(G):
    exact = exact_vertex_cover(G)
    greedy = greedy_vertex_cover(G)
    matching = matching_vertex_cover(G)
    lp_vals = lp_relaxation_vertex_cover(G)
    lp_rounded = round_lp_solution(lp_vals)
    pd = primal_dual_vertex_cover(G)

    exact_size = len(exact)
    return {
        "exact": exact_size,
        "greedy": len(greedy) / exact_size,
        "matching": len(matching) / exact_size,
        "lp_rounding": len(lp_rounded) / exact_size,
        "primal_dual": len(pd) / exact_size,
    }


def experiment_small_sizes():
    """Only feasible for small n, since we need the exact solver."""
    sizes = [4, 6, 8, 10, 12]
    families = {
        "random": lambda n: random_graph(n, 0.4, seed=n),
        "bipartite": lambda n: bipartite_graph(n // 2, n // 2, 0.4, seed=n),
        "complete": lambda n: complete_graph(n),
    }

    results = {fam: {method: [] for method in
                      ["greedy", "matching", "lp_rounding", "primal_dual"]}
               for fam in families}

    for fam_name, gen in families.items():
        for n in sizes:
            G = gen(n)
            res = run_all_methods(G)
            for method in ["greedy", "matching", "lp_rounding", "primal_dual"]:
                results[fam_name][method].append(res[method])

    # Plot: one subplot per family
    fig, axes = plt.subplots(1, len(families), figsize=(15, 5))
    for ax, (fam_name, method_results) in zip(axes, results.items()):
        for method, ratios in method_results.items():
            ax.plot(sizes, ratios, marker="o", label=method)
        ax.set_title(fam_name)
        ax.set_xlabel("n")
        ax.set_ylabel("approximation ratio")
        ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.5)
        ax.legend()

    plt.tight_layout()
    plt.savefig("approximation_ratios.png")
    print("Saved plot to approximation_ratios.png")
    print(results)


if __name__ == "__main__":
    experiment_small_sizes()
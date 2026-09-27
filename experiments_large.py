"""
experiments_large.py
Compares greedy, LP-rounding, and primal-dual on larger graphs where
brute-force exact solving is infeasible. Uses the LP relaxation value
itself as a lower bound on the true optimum, so we can still compute
a bound on the approximation ratio even without the exact answer.
"""

import matplotlib.pyplot as plt
from graphs import random_graph, bipartite_graph, complete_graph
from heuristics import greedy_vertex_cover, matching_vertex_cover
from lp_rounding import lp_relaxation_vertex_cover, round_lp_solution
from primal_dual import primal_dual_vertex_cover


def run_large_methods(G):
    lp_vals = lp_relaxation_vertex_cover(G)
    lp_optimum = sum(lp_vals.values())  # valid lower bound on true optimum

    greedy = greedy_vertex_cover(G)
    lp_rounded = round_lp_solution(lp_vals)
    pd = primal_dual_vertex_cover(G)

    return {
        "greedy": len(greedy) / lp_optimum,
        "lp_rounding": len(lp_rounded) / lp_optimum,
        "primal_dual": len(pd) / lp_optimum,
    }


def experiment_large_sizes():
    sizes = [20, 50, 100, 200, 300]
    families = {
        "random": lambda n: random_graph(n, 0.1, seed=n),
        "bipartite": lambda n: bipartite_graph(n // 2, n // 2, 0.1, seed=n),
        "complete": lambda n: complete_graph(n),
    }

    results = {fam: {method: [] for method in
                      ["greedy", "lp_rounding", "primal_dual"]}
               for fam in families}

    for fam_name, gen in families.items():
        for n in sizes:
            G = gen(n)
            res = run_large_methods(G)
            for method in ["greedy", "lp_rounding", "primal_dual"]:
                results[fam_name][method].append(res[method])
            print(f"{fam_name}, n={n}: {res}")

    fig, axes = plt.subplots(1, len(families), figsize=(15, 5))
    for ax, (fam_name, method_results) in zip(axes, results.items()):
        for method, ratios in method_results.items():
            ax.plot(sizes, ratios, marker="o", label=method)
        ax.set_title(fam_name)
        ax.set_xlabel("n")
        ax.set_ylabel("ratio vs. LP lower bound")
        ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.5)
        ax.legend()

    plt.tight_layout()
    plt.savefig("large_scale_ratios.png")
    print("Saved plot to large_scale_ratios.png")


if __name__ == "__main__":
    experiment_large_sizes()
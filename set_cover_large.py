"""
set_cover_large.py
Compares greedy, LP-rounding, and primal-dual on larger Set Cover instances
where exact solving is infeasible. Uses the LP relaxation value as a lower bound.
"""

import matplotlib.pyplot as plt
from set_cover_instances import random_set_cover_instance
from set_cover_heuristics import greedy_set_cover
from set_cover_lp import lp_relaxation_set_cover, round_lp_set_cover
from primal_dual_fixed import primal_dual_set_cover_fixed as primal_dual_set_cover


def run_large_methods(universe, subsets):
    lp_vals = lp_relaxation_set_cover(universe, subsets)
    lp_optimum = sum(lp_vals)

    greedy = greedy_set_cover(universe, subsets)
    lp_rounded = round_lp_set_cover(lp_vals, universe, subsets)
    pd = primal_dual_set_cover(universe, subsets)

    return {
        "greedy": len(greedy) / lp_optimum,
        "lp_rounding": len(lp_rounded) / lp_optimum,
        "primal_dual": len(pd) / lp_optimum,
    }


def experiment_large_set_cover():
    sizes = [20, 50, 100, 150, 200]
    results = {method: [] for method in ["greedy", "lp_rounding", "primal_dual"]}

    for n in sizes:
        num_sets = n // 2
        max_size = max(3, n // 10)
        universe, subsets = random_set_cover_instance(n, num_sets, max_size, seed=n)
        res = run_large_methods(universe, subsets)
        for method in ["greedy", "lp_rounding", "primal_dual"]:
            results[method].append(res[method])
        print(f"n={n} ({num_sets} subsets, max size {max_size}): {res}")

    fig, ax = plt.subplots(figsize=(8, 5))
    for method, ratios in results.items():
        ax.plot(sizes, ratios, marker="o", label=method)
    ax.set_xlabel("Universe size (n)")
    ax.set_ylabel("Ratio vs. LP lower bound")
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.5)
    ax.legend()
    ax.set_title("Set Cover at scale: ratio vs. LP lower bound")

    plt.tight_layout()
    plt.savefig("set_cover_large_ratios.png")
    print("Saved plot to set_cover_large_ratios.png")


if __name__ == "__main__":
    experiment_large_set_cover()
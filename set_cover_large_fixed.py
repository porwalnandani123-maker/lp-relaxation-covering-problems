"""
set_cover_large_fixed.py
Same as set_cover_large.py, but holds max subset size FIXED
while universe size grows, to isolate the effect of scale alone
from the effect of larger subsets (frequency).
"""

import matplotlib.pyplot as plt
from set_cover_instances import random_set_cover_instance
from set_cover_heuristics import greedy_set_cover
from set_cover_lp import lp_relaxation_set_cover, round_lp_set_cover
from set_cover_primal_dual import primal_dual_set_cover


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


def experiment_fixed_subset_size():
    sizes = [20, 50, 100, 150, 200]
    fixed_max_size = 5  # held constant this time
    results = {method: [] for method in ["greedy", "lp_rounding", "primal_dual"]}

    for n in sizes:
        num_sets = n // 2
        universe, subsets = random_set_cover_instance(n, num_sets, fixed_max_size, seed=n)
        res = run_large_methods(universe, subsets)
        for method in ["greedy", "lp_rounding", "primal_dual"]:
            results[method].append(res[method])
        print(f"n={n} ({num_sets} subsets, fixed max size {fixed_max_size}): {res}")

    fig, ax = plt.subplots(figsize=(8, 5))
    for method, ratios in results.items():
        ax.plot(sizes, ratios, marker="o", label=method)
    ax.set_xlabel("Universe size (n)")
    ax.set_ylabel("Ratio vs. LP lower bound")
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.5)
    ax.legend()
    ax.set_title(f"Set Cover at scale, fixed max subset size = {fixed_max_size}")

    plt.tight_layout()
    plt.savefig("set_cover_fixed_size_ratios.png")
    print("Saved plot to set_cover_fixed_size_ratios.png")


if __name__ == "__main__":
    experiment_fixed_subset_size()
    
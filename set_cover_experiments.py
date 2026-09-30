"""
set_cover_experiments.py
Compares greedy, LP-rounding, and primal-dual for Set Cover
against the exact solution, across several random instances.
"""

import matplotlib.pyplot as plt
from set_cover_instances import random_set_cover_instance
from set_cover_exact import exact_set_cover
from set_cover_heuristics import greedy_set_cover
from set_cover_lp import lp_relaxation_set_cover, round_lp_set_cover
from primal_dual_fixed import primal_dual_set_cover_fixed as primal_dual_set_cover


def run_all_methods(universe, subsets):
    exact = exact_set_cover(universe, subsets)
    greedy = greedy_set_cover(universe, subsets)
    lp_vals = lp_relaxation_set_cover(universe, subsets)
    lp_rounded = round_lp_set_cover(lp_vals, universe, subsets)
    pd = primal_dual_set_cover(universe, subsets)

    exact_size = len(exact)
    return {
        "exact": exact_size,
        "greedy": len(greedy) / exact_size,
        "lp_rounding": len(lp_rounded) / exact_size,
        "primal_dual": len(pd) / exact_size,
    }


def experiment_set_cover():
    # Keep num_sets small since exact solver is brute-force
    configs = [
        (10, 5, 4),
        (10, 6, 4),
        (10, 7, 4),
        (12, 7, 5),
        (12, 8, 5),
    ]

    results = {method: [] for method in ["greedy", "lp_rounding", "primal_dual"]}
    labels = []

    for i, (num_elements, num_sets, max_size) in enumerate(configs):
        universe, subsets = random_set_cover_instance(
            num_elements, num_sets, max_size, seed=i
        )
        res = run_all_methods(universe, subsets)
        labels.append(f"{num_elements}e/{num_sets}s")
        for method in ["greedy", "lp_rounding", "primal_dual"]:
            results[method].append(res[method])
        print(f"Config {labels[-1]}: {res}")

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(configs))
    for method, ratios in results.items():
        ax.plot(x, ratios, marker="o", label=method)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_xlabel("Instance (elements/subsets)")
    ax.set_ylabel("Approximation ratio")
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.5)
    ax.legend()
    ax.set_title("Set Cover: approximation ratio vs. exact optimum")

    plt.tight_layout()
    plt.savefig("set_cover_ratios.png")
    print("Saved plot to set_cover_ratios.png")


if __name__ == "__main__":
    experiment_set_cover()
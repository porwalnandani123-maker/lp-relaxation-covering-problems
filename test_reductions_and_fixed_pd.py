"""
test_reductions_and_fixed_pd.py

1. Hand-checkable test of set_cover_reductions.reduce_instance on a tiny instance.
2. Reduction stats (R1-R3) across a range of instance sizes, mirroring the
   Nemhauser-Trotter density sweep done for Vertex Cover.
3. Re-run the Vertex Cover and Set Cover comparison experiments using
   primal_dual_fixed instead of the original (buggy) primal_dual, to quantify
   how much the dual-infeasibility bug affected earlier reported ratios.
"""

from set_cover_instances import random_set_cover_instance
from set_cover_exact import exact_set_cover
from set_cover_heuristics import greedy_set_cover
from set_cover_lp import lp_relaxation_set_cover, round_lp_set_cover
from set_cover_reductions import reduce_instance, persistency_holds
from primal_dual_fixed import primal_dual_set_cover_fixed, primal_dual_vertex_cover_fixed
from graphs import random_graph, complete_graph
from exact import exact_vertex_cover


def hand_checkable_test():
    """
    Universe = {1,2,3,4}. Sets:
      S0 = {1}       -> element 1 only covered here: R1 should force S0 in.
      S1 = {2,3}
      S2 = {2,3,4}   -> S1 subset of S2: R2 should drop S1.
    Expected: forced = [0], reduced universe = {4} (after S1 dropped, only
    S2 covers 2,3,4; but 2 and 3 become redundant once S2 is the sole survivor
    for them -- trace by hand and compare to the R3 result you actually get).
    """
    universe = [1, 2, 3, 4]
    subsets = [{1}, {2, 3}, {2, 3, 4}]

    forced, red_universe, red_subsets, imap = reduce_instance(universe, subsets)
    print("Hand-checkable test:")
    print(f"  forced (original indices): {forced}")
    print(f"  reduced universe: {red_universe}")
    print(f"  reduced subsets: {red_subsets}")
    print(f"  index map: {imap}")
    print("  Expected: forced includes 0 (S0, from R1).")
    print("  Verify the rest by hand before trusting this on larger instances.\n")


def reduction_stats_sweep():
    print("--- Set Cover reduction stats across sizes ---")
    for n in [10, 20, 30, 40, 50]:
        universe, subsets = random_set_cover_instance(n, n // 2, max(3, n // 8), seed=n)
        forced, red_universe, red_subsets, imap = reduce_instance(universe, subsets)
        orig_elems, orig_sets = len(universe), len(subsets)
        red_elems, red_sets = len(red_universe), len(red_subsets)
        elem_reduction = 100 * (1 - red_elems / orig_elems) if orig_elems else 0
        set_reduction = 100 * (1 - red_sets / orig_sets) if orig_sets else 0
        print(f"n={n}: elements {orig_elems}->{red_elems} ({elem_reduction:.1f}% cut), "
              f"sets {orig_sets}->{red_sets} ({set_reduction:.1f}% cut), forced {len(forced)}")
    print()


def persistency_check():
    print("--- LP-fixing persistency check (Set Cover) ---")
    for n in [10, 15, 20]:
        universe, subsets = random_set_cover_instance(n, n // 2, max(3, n // 6), seed=n + 100)
        from set_cover_reductions import lp_fixing
        x, fin, fout = lp_fixing(universe, subsets)
        holds = persistency_holds(universe, subsets, fin, fout)
        print(f"n={n}: forced_in={len(fin)}, forced_out={len(fout)}, persistency holds: {holds}")
    print()


def compare_old_vs_fixed_primal_dual():
    print("--- Old (buggy) vs fixed primal-dual: Vertex Cover ---")
    from primal_dual import primal_dual_vertex_cover as old_pd_vc
    for name, g in [
        ("Random(10)", random_graph(10, 0.4, seed=1)),
        ("Complete(6)", complete_graph(6)),
    ]:
        exact = len(exact_vertex_cover(g))
        old = len(old_pd_vc(g))
        fixed = len(primal_dual_vertex_cover_fixed(g))
        print(f"{name}: exact={exact}, old primal-dual={old} (ratio {old/exact:.2f}), "
              f"fixed primal-dual={fixed} (ratio {fixed/exact:.2f})")

    print("\n--- Old (buggy) vs fixed primal-dual: Set Cover ---")
    from set_cover_primal_dual import primal_dual_set_cover as old_pd_sc
    for n in [10, 15, 20]:
        universe, subsets = random_set_cover_instance(n, n // 2, max(3, n // 6), seed=n)
        exact = len(exact_set_cover(universe, subsets))
        old = len(old_pd_sc(universe, subsets))
        fixed = len(primal_dual_set_cover_fixed(universe, subsets))
        print(f"n={n}: exact={exact}, old={old} (ratio {old/exact:.2f}), "
              f"fixed={fixed} (ratio {fixed/exact:.2f})")


if __name__ == "__main__":
    hand_checkable_test()
    reduction_stats_sweep()
    persistency_check()
    compare_old_vs_fixed_primal_dual()
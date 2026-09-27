# LP Relaxation and Rounding for NP-Hard Covering Problems

Empirical study of approximation algorithms for Vertex Cover (and, in progress, Set Cover):
greedy, maximal-matching, LP relaxation with rounding, and primal-dual — compared against
exact solutions across graph families.

## Status
- Vertex Cover: all four methods implemented and tested (this section below).
- Set Cover: in progress.
- Nemhauser-Trotter preprocessing and larger-scale experiments: planned next.

## Files
- `graphs.py` — generates random, bipartite, and complete graph instances
- `exact.py` — brute-force exact Vertex Cover solver (small instances only)
- `heuristics.py` — greedy and maximal-matching algorithms
- `lp_rounding.py` — LP relaxation, rounding, and half-integrality check
- `primal_dual.py` — primal-dual 2-approximation algorithm
- `experiments.py` — runs all methods across graph families and sizes, produces plots

## Key findings so far

1. **Bipartite graphs confirm LP integrality.** Greedy and LP-rounding both achieve
   ratio 1.0 across all tested sizes, matching the theorem that Vertex Cover's LP
   relaxation is exactly integral on bipartite graphs.

2. **Complete graphs follow an exact n/(n-1) pattern.** Matching, LP-rounding, and
   primal-dual all produce a cover of size n (all vertices), against a true optimum
   of n-1, giving ratio n/(n-1) — which *shrinks toward 1* as n grows. This refines
   the textbook 2x worst-case bound: that bound is tightest for small dense graphs,
   not large complete graphs. Greedy alone finds the exact optimum on complete graphs.

3. **On random graphs, LP-rounding shows the narrowest spread of ratios**
   (worst case 1.6x in this sample, versus 2.0x for matching and 2.5x for primal-dual),
   suggesting it is the more reliable choice absent structural guarantees, even though
   the classical bound does not distinguish between the methods.

![Approximation ratios](approximation_ratios.png)

## Next steps
- Extend experiments to larger n (skip exact solver, compare heuristics only)
- Implement Nemhauser-Trotter preprocessing
- Repeat this study for Set Cover
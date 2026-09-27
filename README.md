# LP Relaxation and Rounding for NP-Hard Covering Problems

Empirical study of approximation algorithms for Vertex Cover (and, in progress, Set Cover):
greedy, maximal-matching, LP relaxation with rounding, and primal-dual — compared against
exact solutions across graph families.

## Status
- Vertex Cover: all four methods implemented and tested, at both small and large scale.
- Set Cover: in progress.
- Nemhauser-Trotter preprocessing: planned next.

## Files
- `graphs.py` — generates random, bipartite, and complete graph instances
- `exact.py` — brute-force exact Vertex Cover solver (small instances only)
- `heuristics.py` — greedy and maximal-matching algorithms
- `lp_rounding.py` — LP relaxation, rounding, and half-integrality check
- `primal_dual.py` — primal-dual 2-approximation algorithm
- `experiments.py` — small-scale experiments against the true optimum
- `experiments_large.py` — large-scale experiments against the LP lower bound

## Key findings (small scale, vs. true optimum)

1. **Bipartite graphs confirm LP integrality.** Greedy and LP-rounding both achieve
   ratio 1.0 across all tested sizes, matching the theorem that Vertex Cover's LP
   relaxation is exactly integral on bipartite graphs.

2. **Complete graphs follow an exact n/(n-1) pattern.** Matching, LP-rounding, and
   primal-dual all produce a cover of size n, against a true optimum of n-1, giving
   ratio n/(n-1) — which *shrinks toward 1* as n grows. This refines the textbook 2x
   worst-case bound: that bound is tightest for small dense graphs, not large complete
   graphs. Greedy alone finds the exact optimum on complete graphs.

3. **On random graphs, LP-rounding shows the narrowest spread of ratios**
   (worst case 1.6x in this sample, versus 2.0x for matching and 2.5x for primal-dual).

![Approximation ratios](approximation_ratios.png)

## Large-scale findings (vs. LP lower bound)

Exact solving is infeasible beyond ~20 nodes, so at larger sizes we compare methods
against the **LP relaxation value** instead of the true optimum. This bound is valid
(LP optimum ≤ true optimum) but can be loose, which changes what the ratios mean:

- **On complete graphs, greedy's ratio rises toward 2** in this plot, which looks like
  a contradiction of the small-scale result (where greedy was exact, ratio 1.0). It
  isn't: the LP optimum on a complete graph is n/2, while the true optimum is n-1, so
  even an exact algorithm shows ratio ≈ (n-1)/(n/2) ≈ 2 here. The apparent gap reflects
  the bound's looseness on this family, not greedy's actual performance.
- **On bipartite graphs**, LP-rounding stays flat at 1.0, since the LP bound equals the
  true optimum here — this plot's ratio is the real ratio for this family.
- **On random graphs**, LP-rounding and primal-dual both climb to and flatten at the
  worst-case bound of 2.0 as n grows, while greedy grows more slowly, though its ratio
  here is also inflated by the same bound-looseness effect as complete graphs.

![Large-scale ratios](large_scale_ratios.png)

## Next steps
- Implement Nemhauser-Trotter preprocessing
- Repeat this study for Set Cover
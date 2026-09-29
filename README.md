# LP Relaxation and Rounding for NP-Hard Covering Problems

Empirical study of approximation algorithms for Vertex Cover and Set Cover:
greedy, maximal-matching, LP relaxation with rounding, and primal-dual — compared against
exact solutions across graph families.

## Status
- Vertex Cover: all four methods implemented and tested, at both small and large scale,
  plus Nemhauser-Trotter preprocessing.
- Set Cover: in progress.

## Files
- `graphs.py` — generates random, bipartite, and complete graph instances
- `exact.py` — brute-force exact Vertex Cover solver (small instances only)
- `heuristics.py` — greedy and maximal-matching algorithms
- `lp_rounding.py` — LP relaxation, rounding, and half-integrality check
- `primal_dual.py` — primal-dual 2-approximation algorithm
- `nemhauser_trotter.py` — LP-based preprocessing to fix vertices before rounding
- `experiments.py` — small-scale experiments against the true optimum
- `experiments_large.py` — large-scale experiments against the LP lower bound
- `set_cover_instances.py` — generates Set Cover instances (in progress)

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

## Nemhauser-Trotter preprocessing

Tested at n=30 across a range of edge probabilities to see how graph density affects
how much the LP relaxation can resolve on its own:

| Edge probability (p) | Nodes | Edges | Size reduction | Forced in / out |
|---|---|---|---|---|
| 0.05 | 30 | 23 | 76.7% | 7 / 16 |
| 0.10 | 30 | 51 | 23.3% | 3 / 4 |
| 0.15 | 30 | 78 | 6.7% | 1 / 1 |
| 0.20 | 30 | 102 | 0.0% | 0 / 0 |

**Reduction drops sharply as graphs get denser.** At p=0.05 (sparse), three-quarters of
vertices are resolved by the LP alone; by p=0.2, none are. This makes sense: in a sparse
graph, many vertices have few or no edges, so the LP relaxation can push their value to
exactly 0 or 1 without ambiguity. As density increases, more vertices get pulled into
genuinely undecided (0.5) territory, since they're now competing over shared edges with
no clear-cut assignment.

The earlier tests (random graph at p=0.3, and the complete graph) both showed 0%
reduction, consistent with this trend — both are on the denser end of the spectrum.
This suggests Nemhauser-Trotter is most useful as a preprocessing step for sparse
instances, and of little help on dense ones, where the reduction to an approximation
algorithm still has to handle nearly the full-size problem.

## Set Cover findings

Tested greedy, LP-rounding, and primal-dual against the exact optimum across 5 random
instances (10-12 elements, 5-8 subsets, max subset size 4-5):

| Instance | Exact | Greedy ratio | LP-rounding ratio | Primal-dual ratio |
|---|---|---|---|---|
| 10 elements / 5 subsets | 6 | 1.0 | 1.0 | 1.17 |
| 10 elements / 6 subsets | 4 | 1.0 | 1.0 | 1.5 |
| 10 elements / 7 subsets | 7 | 1.0 | 1.0 | 1.14 |
| 12 elements / 7 subsets | 5 | 1.0 | 1.0 | 1.2 |
| 12 elements / 8 subsets | 5 | 1.0 | 1.0 | 1.2 |

**Greedy and LP-rounding find the exact optimum on every tested instance**, while
**primal-dual is consistently worse** (1.14x-1.5x). This differs from the Vertex Cover
results, where no single method dominated across all graph families — here, two of the
three methods are uniformly strong on this sample. A larger and more varied sample of
instances would be needed to confirm this holds generally, since 5 instances is a small
sample and greedy in particular has no general worst-case guarantee better than the
proven O(log n) bound.

![Set Cover ratios](set_cover_ratios.png)

## Set Cover at scale (vs. LP lower bound)

| n | Subsets | Max subset size | Greedy | LP-rounding | Primal-dual |
|---|---|---|---|---|---|
| 20 | 10 | 3 | 1.0 | 1.0 | 1.07 |
| 50 | 25 | 5 | 1.0 | 1.0 | 1.03 |
| 100 | 50 | 10 | 1.0 | 1.0 | 1.48 |
| 150 | 75 | 15 | 1.07 | 1.34 | 1.58 |
| 200 | 100 | 20 | 1.16 | 1.81 | 1.92 |

**Primal-dual is the weakest method at every tested size**, and the gap between methods
widens as n grows. Greedy and LP-rounding start at the LP bound exactly (ratio 1.0) for
small instances, but all three degrade as n increases.

**Caveat:** in this experiment, max subset size grows alongside n (3 at n=20, up to 20
at n=200), so scale and subset size increase together. Since the LP-rounding bound
depends on the maximum element frequency f, larger subsets could independently loosen
the LP bound, confounding the effect of scale alone. Isolating the two — testing fixed
subset size across growing n — is a natural next step to confirm whether this trend is
driven by scale, subset size, or both.

![Set Cover large-scale ratios](set_cover_large_ratios.png)

## Next steps
- Compare Vertex Cover (as a special case) against general Set Cover instances
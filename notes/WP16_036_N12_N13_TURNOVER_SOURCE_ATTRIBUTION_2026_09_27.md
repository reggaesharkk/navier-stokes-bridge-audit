# WP16 N12/N13 K36 turnover source-orbit attribution

Prince Upadhyay, Independent Research — post-hoc finite-Galerkin diagnostic, 27 September 2026

## Boundary

This analysis was performed after the N12/N13 trajectory outcomes and after the later N14–N16 prospective tests were known. It is therefore **post-hoc mechanism analysis**, not a new holdout. The N11-derived K36 coalition, the archived N12/N13 phase states, and all frozen pass/fail thresholds are left unchanged.

The question is narrower than persistence: for the K36 absolute-mass margin

`F = I - 9 O`,

where `I` is the grouped absolute mass inside the frozen 36 ordered source-orbit pairs and `O` is the corresponding outside mass, what makes the instantaneous Galerkin RHS rate `F'` turn from positive at the anchor to negative early in the trajectory?

## Reproduction and provenance

The reproduction script is `src/wp16_036_N12_N13_turnover_attribution.py`. It reconstructs the archived N12 and N13 `inherited`, `target_only`, and `full_final` states, evolves each with the already-audited dealiased Galerkin solver on `dt=0.0001` through `t=0.001`, and computes centered directional derivatives along the instantaneous Galerkin RHS. It does not optimize phases or alter K36.

Pinned canonical inputs, using LF-normalized hashes for JSON text so Windows line endings do not create false failures:

- N10/N11 continuation: `34a10cf119ab6614c46d29540c4d4701eab082229582fb0a8189add0cd8f96a5`
- N12 continuation: `ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855`
- N13 continuation: `13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd`
- original source-decomposition JSON: `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`
- canonical compressed source archive: `ab238d8df279eb925cf8145cb33cb5670513aea61a2547a1ac0a7ae1b1493f95`

The checked compact output is `results/wp16_n13_holdout/K36_turnover_source_rates_N12_N13.json` with SHA-256 `8d5f9b93280e5f3c3a6fb73cb62460a2995a0871ce056de5e21864b5445fe86d`.

At the anchor, the six reconstructed `F'` values agree with the previously archived `K36_margin_velocity_N12_N13.json` full-RHS derivative values to maximum absolute difference `6.51e-5`. A four-scale directional check for N13 `inherited` at the anchor gives:

| central-difference step | `F'` |
|---:|---:|
| `5e-9` | 208744.06746419077 |
| `1e-8` | 208744.06744890657 |
| `2e-8` | 208744.06744872584 |
| `4e-8` | 208744.06745779893 |

The full spread is about `1.55e-5` on a derivative of about `2.09e5`.

## The early turnover

At `t=0`, all six margins are increasing. By `t=0.001`, all six have negative instantaneous margin rate even though the inside-K36 absolute mass is still increasing:

| cutoff | state | `I'(0.001)` | `O'(0.001)` | `F'(0)` | `F'(0.001)` |
|---|---|---:|---:|---:|---:|
| N12 | inherited | +82,978.875 | +37,243.395 | +401,321.345 | **−252,211.678** |
| N12 | target_only | +82,984.418 | +37,238.027 | +401,330.158 | **−252,157.821** |
| N12 | full_final | +212,112.718 | +49,727.978 | +209,854.161 | **−235,439.081** |
| N13 | inherited | +184,492.903 | +50,077.037 | +208,744.067 | **−266,200.434** |
| N13 | target_only | +56,749.214 | +38,729.845 | +187,391.873 | **−291,819.387** |
| N13 | full_final | +67,719.361 | +34,063.935 | +121,276.530 | **−238,856.054** |

Thus the observed finite-trajectory turnover is not caused by `I` shrinking at `t=0.001`. It is caused by positive outside growth becoming large enough that `9 O' > I'`.

The first sampled sign changes of the instantaneous rates are:

| cutoff | state | first sampled `F'<0` | first sampled positive rate of common leading outside group |
|---|---|---:|---:|
| N12 | inherited | 0.0004 | 0.0003 |
| N12 | target_only | 0.0004 | 0.0003 |
| N12 | full_final | 0.0005 | 0.0005 |
| N13 | inherited | 0.0005 | 0.0005 |
| N13 | target_only | 0.0004 | 0.0004 |
| N13 | full_final | 0.0007 | 0.0009 |

These are sampled finite-grid observations, not certified continuous turnover times.

## A common outside-growth motif

At `t=0.001`, the same ordered source-orbit pair is the **rank-1 positive outside absolute-mass rate in all six states**:

`([3,3,4], [0,2,3])`.

Its positive outside-mass rate and share of the *net* outside rate are:

| cutoff | state | group rate | group rate / net `O'` |
|---|---|---:|---:|
| N12 | inherited | +13,224.116 | 35.51% |
| N12 | target_only | +13,224.359 | 35.51% |
| N12 | full_final | +13,445.567 | 27.04% |
| N13 | inherited | +13,260.982 | 26.48% |
| N13 | target_only | +12,044.980 | 31.10% |
| N13 | full_final | +9,597.679 | 28.18% |

The five largest positive outside-group rates account for about 74.87%, 74.88%, 53.93%, 52.02%, 58.35%, and 58.67% of the corresponding net outside rates. Because negative-rate outside groups also exist, these percentages are descriptive shares of the net derivative and are not a partition of a positive measure.

Eight ordered groups appear in the top ten positive outside-growth ranks in **all six** `t=0.001` snapshots. The first three are especially stable:

| ordered source-orbit pair | top-10 occurrence | mean rank | mean rate |
|---|---:|---:|---:|
| `([3,3,4],[0,2,3])` | 6/6 | 1.00 | 12,466.28 |
| `([1,2,2],[2,5,7])` | 6/6 | 2.00 | 4,221.24 |
| `([1,4,4],[1,1,2])` | 6/6 | 3.00 | 3,475.52 |
| `([4,4,5],[1,1,4])` | 6/6 | 5.17 | 2,395.62 |
| `([2,3,3],[0,2,3])` | 6/6 | 6.17 | 2,156.91 |
| `([0,2,3],[2,3,9])` | 6/6 | 6.83 | 1,956.62 |
| `([1,1,2],[1,2,8])` | 6/6 | 7.00 | 1,910.32 |
| `([2,3,3],[0,3,4])` | 6/6 | 7.33 | 1,794.87 |

These rankings are post-hoc descriptions and are **not** a new frozen coalition.

## What the leading group does — and does not explain

The rank-1 group `([3,3,4],[0,2,3])` is shrinking at the anchor in all six states and later becomes a strong positive outside-growth contributor. It therefore identifies a common late accelerator of outside mass.

It is **not** a universal trigger for the onset of negative `F'`. The clearest counterexample is N13 `full_final`: its sampled `F'` first becomes negative at `t=0.0007`, while the leading group's own absolute-mass rate remains negative until the `t=0.0009` sample. Other outside groups and the balance with `I'` can reverse the margin before this one group turns positive.

The correct finite-data statement is therefore: a small recurrent family of outside groups, headed by `([3,3,4],[0,2,3])`, dominates the later outside-growth budget by `t=0.001`, but the onset of the K36-margin turnover is collective and state-dependent.

## Connection to the later N16 attribution

The same ordered pair `([3,3,4],[0,2,3])` reappears in the independent post-hoc N16 source-orbit accounting. At the critical N16 `t=0.0023` sample it is the largest outside difference between `full_final` and `inherited`: its normalized absolute mass is `13.79519` in inherited versus `9.28693` in full_final, a difference of `−4.50827`, slightly larger in magnitude than the entire net outside difference `ΔO=−4.44520`.

That recurrence is mechanistically suggestive but must be interpreted with the N16 denominator audit. The grouped diagnostic is `g_j = Im(C_j/z)`, and the tracked complex normalizer `z` changes with state. In the N16 comparison at `t=0.0023`, the aggregate outside swap decomposes as approximately `+0.85803` from the complex group numerators and `−5.30322` from the tracked normalizer, yielding the observed `ΔO=−4.44520`. Therefore the N16 advantage cannot be described as universal physical suppression of outside triads.

Taken together, N12/N13 and N16 point to the next analytic target: track the evolution of the **unnormalized complex source numerators and the complex normalizer `z` jointly**, rather than treating normalized group absolute masses as standalone physical source strengths.

## Scope

This audit explains a repeatable source-resolved pattern in six reconstructed finite N12/N13 trajectories and relates it to one later finite N16 comparison. It does not prove that these orbit families dominate at arbitrary cutoffs, bound their time integral, establish a cutoff-uniform K36 estimate, or imply regularity or blowup for the three-dimensional Navier–Stokes equations.

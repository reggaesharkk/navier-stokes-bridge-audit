# M14/M15 duality compatibility audit

**Date:** 2026-10-02  
**Disposition:** `PARTIAL_M15_FORCED_RADIUS_COMPUTED; ADJOINT_WEIGHTED_REMAINDER_OPEN`  
**Purpose:** determine whether the frozen M14 dual integral can be combined with the existing goal-weighted uncertainty and endpoint bounds.

## Decision

The frozen signed integral is valid for the saved M14 cubic reconstruction embedded in the M15 system. It is not reconciled with the earlier endpoint/uncertainty bounds: those bounds used an M14 predictor-error radius, while the dual residual drives the difference between the M15 trajectory and that embedded M14 reconstruction.

The missing full-space radius has now been computed from the frozen residuals and whole-segment gradient bounds using a standard L2 difference-energy inequality. The resulting outward terminal radius is 10.559636070809868141657764813075. This closes the missing L2-radius input only. It does not close the adjoint-weighted defect, quadratic objective remainder, endpoint transfer, or normalizer gate.

This is a compatibility and coverage correction. It does not show either frozen computation is numerically wrong and does not establish a failure of the finite-observable transfer.

## Frozen evidence

- Dual quadrature: `PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY`, all 240 half-steps, interval `[5758574435.605829673039071, 5758574435.605829673039791]`.
- Aggregate SHA-256: `8b3a7806e462786b887c635f1e6dbd323faadf8c5e0dedd42143969afebf75a3`.
- Its six frozen input hashes match the input identities bound by the goal-weighted full-path computation.
- Goal-weighted computation: `PASS_RECONSTRUCTION_GOAL_WEIGHTED_PRIMAL_TUBE_ONLY`; interior M14 predictor-tube allowance `3368.516639829895`, terminal boundary product `277957977.931533676582`.
- The wider previously recorded endpoint/Taylor plus interior allowance is `282300477.131407882477`.

The raw scale comparison is diagnostic only: the signed integral is about 20.4 times the wider recorded allowance. Those quantities cannot be combined because the earlier uncertainty bound did not cover the M15 difference path.

## Identity and M15 forced radius

Let U(t) be the embedded M14 reconstruction, Y(t) the M15 solution from the same initial datum, e=Y-U, F15 the M15 vector field, and R=F15(U)-U_t. For the Navier-Stokes difference equation, transport by U and self-transport by e cancel in the L2 energy pairing; viscosity is dissipative. Therefore, with M(t) bounding the pointwise gradient of U:

`d ||e||_2 / dt <= M(t) ||e||_2 + ||R||_2`.

The replay uses the frozen M14 whole-segment `gradient_Fourier_l1_upper_decimal` bound for M on each pair of half-steps and the frozen full-M15 `primal_defect_L2_upper` bound for R on each half-step. It starts with E0=0 and applies:

`E[n+1] = exp(M[n] h) E[n] + R[n] (exp(M[n] h)-1) / M[n]`, with `h=1/80000`.

All input decimal strings are outward upper bounds. The exponential is bounded with an exact rational degree-20 Taylor sum plus a geometric upper bound on its positive tail. The replay verifies all 12 shards, identical frozen input hashes, and exact step coverage 0–239. It obtains terminal radius `10.559636070809868141657764813075`; maximum segment gradient bound is `2486.991992`. For scale only, this is about 178,248 times the earlier M14 terminal tube radius `0.000059241340007`; the two radii refer to different error equations, so this ratio is not a certification comparison.

The result is `PASS_M15_FORCED_L2_RADIUS_ONLY`. It bounds Y-U in M15 L2 under the frozen segment majorants. It is intentionally not treated as an objective-transfer bound.

## M15 weighted-remainder outcome

The frozen 12 goal-weighted shards were replayed against the M15 radius. The replay recovered each original Young coefficient from its outward quadratic bound using a strict lower bound on the serialized M14 radius, then enlarged the support factor to cover all 14,147 M15 modes. The enlargement factor is `1.108505684201276629860741121330`.

| Term | Outward upper bound |
|---|---:|
| Adjoint-defect integral | `240063.832492240296` |
| Quadratic remainder with M15 support | `114517700895378.757870383616` |
| Terminal saved-adjoint boundary product | `49545386543507.498269542068` |
| Sum of these three terms | `164063087678950.088632165980` |
| Frozen signed-integral lower bound | `5758574435.605829673039071` |
| Signed lower bound minus remainder sum | `-164057329104514.482802492940` |

Status: `NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS`. The current conservative bounds do not preserve the sign. The quadratic term dominates; it is also the coarsest part because the replay recovers a coefficient from already rounded per-step outputs. The final 20 half-steps (220–239) contribute about 69.6% of that quadratic upper bound, so they are the highest-value place to sharpen first while preserving full-path coverage. This is a failure to close the current certificate budget, not evidence that the underlying finite-observable transfer is false.

The frozen signed integral and all source artifacts remain unchanged. The weighted result is stored at [m15_weighted_remainder.json](m15_weighted_remainder.json), with its exact-rational replay in `src/wp19_v0_28_m15_weighted_remainder_replay.py`.

## Next gate

The useful next computation is a sharper goal-oriented enclosure for the quadratic remainder and terminal pairing. The present global M15 L2 tube is too coarse to carry the sign, even though it safely includes the cutoff defect. Keep the outcome fail-closed until a sharper bound is derived and replayed; then re-evaluate the independent normalizer gate.

## Reproduction

Run the new standard-library replay against the extracted frozen lower-path artifact and the 12 dual shard JSONs:

`python src/wp19_v0_28_m15_forced_radius_replay.py --lower-dir LOWER_DIR --dual-dir DUAL_DIR --output m15_forced_radius.json`

The replay strips only the known legacy two-character trailer from shard files; all other content is parsed as strict JSON. The result is stored at [m15_forced_radius.json](m15_forced_radius.json).

The runner and result hashes are recorded in `results/wp19_v0_28/duality_compatibility_audit_20261002/SHA256SUMS.txt`.

## Source audit

- `src/wp19_v0_28_reconstructed_dual_integral_fullpath_shard.py` and `src/wp19_v0_28_reconstructed_dual_integral_pilot.py`: residual is built in the M15 system from the embedded M14 cubic reconstruction.
- `src/wp19_v0_28_goal_weighted_primal_uncertainty_fullpath.py`: the previous `delta` is the lower-path M14 radius plus reconstruction distance.
- `src/wp19_v0_28_adjoint_segment_arb.py`: `old_radius_and_identity` validates and replays the M14 predictor recurrence.
- `src/wp19_v0_28_m15_forced_radius_replay.py`: exact rational replay of the full M15 L2 forced-radius recurrence.

The dual quadrature freeze remains unchanged. This addendum does not certify the adjoint-weighted remainder, terminal objective transfer, normalizer, cutoff-wide conclusion, or continuum regularity.

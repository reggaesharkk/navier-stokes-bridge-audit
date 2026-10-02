# M14/M15 duality compatibility audit

**Date:** 2026-10-02  
**Disposition:** `BLOCKED_MISSING_M15_ERROR_RADIUS`  
**Purpose:** determine whether the frozen M14 dual integral can be combined with the existing goal-weighted uncertainty and endpoint bounds.

## Decision

The frozen signed integral is valid for the saved M14 cubic reconstruction embedded in the M15 system. It is **not yet reconciled** with the existing endpoint/uncertainty bounds. Source inspection found that those bounds use an M14 predictor-error radius, while the dual residual drives the difference between the M15 trajectory and that embedded M14 reconstruction. The required M15 error radius is absent.

This is a missing-hypothesis/coverage issue. It does not show that either frozen computation is numerically wrong, and it does not establish a failure of the finite-observable transfer.

## Frozen evidence

- Dual quadrature: `PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY`, all 240 half-steps, interval
  `[5758574435.605829673039071, 5758574435.605829673039791]`.
- Aggregate SHA-256: `8b3a7806e462786b887c635f1e6dbd323faadf8c5e0dedd42143969afebf75a3`.
- Its six frozen input hashes match the input identities bound by the goal-weighted full-path computation.
- Goal-weighted computation: `PASS_RECONSTRUCTION_GOAL_WEIGHTED_PRIMAL_TUBE_ONLY`; interior primal-tube allowance `3368.516639829895`, terminal boundary product `277957977.931533676582`.
- The wider previously recorded endpoint/Taylor plus interior allowance is `282300477.131407882477`.

The raw scale comparison is useful as a diagnostic only: the signed integral is about 20.4 times the wider recorded allowance. The values cannot be treated as a contradiction or combined into a theorem until the state-error quantity in the identity is enclosed in the same M15 space.

## Identity and uncovered term

Let (U(t)) be the embedded M14 reconstruction, (Y(t)) the M15 solution from the same initial datum, (e=Y-U), (F_{15}) the M15 vector field, and (R=F_{15}(U)-U_t). Let (lambda) be the saved adjoint and (d=lambda_t+DF_{15}(U)^*lambda) its adjoint defect. With the quadratic Taylor remainder (Q(e)),

[
e_t=DF_{15}(U)e+R+Q(e),
]

and therefore

[
int_0^T langlelambda,Rangle,dt
=langlelambda(T),e(T)angle-langlelambda(0),e(0)angle
-int_0^Tlangle d,eangle,dt
-int_0^Tlanglelambda,Q(e)angle,dt.
]

The goal-weighted source computes its `delta` from `old_radius_and_identity`, which replays the lower-cutoff M14 recurrence from M14 segment residuals. That quantity can cover the M14 predictor's error under the M14 dynamics; it does not cover the M15 error (Y-U), including the newly opened M15 shell forced by (R).

The dual-integral pilot explicitly forms (R) in the high M15 system from the embedded M14 reconstruction. Thus the path-error bound needed by the identity must include this cutoff-defect forcing. The existing M14 tube radius cannot be substituted for it.

## Next gate

Keep the quadrature freeze unchanged. Before any transfer claim:

1. Construct an outward M15 radius for (e=Y-U) over all half-steps, initialized at zero and driven by the full M15 residual (R).
2. Bound the M15 variational growth and nonlinear remainder on that same tube.
3. Recompute the adjoint-defect and quadratic terms with that radius.
4. Reconcile the resulting endpoint identity using outward intervals, then separately pass the normalizer-transfer gate.

No multi-hour rerun is warranted for this diagnosis. The next computation is only the missing M15 forced-radius enclosure; if its majorant cannot close, record the transfer gate as unevaluable/fail-closed.

## Reproduction sources

- `src/wp19_v0_28_reconstructed_dual_integral_fullpath_shard.py` and `src/wp19_v0_28_reconstructed_dual_integral_pilot.py`: residual is built in the M15 system from the embedded M14 cubic reconstruction.
- `src/wp19_v0_28_goal_weighted_primal_uncertainty_fullpath.py`: `delta` is the lower-path radius plus reconstruction distance.
- `src/wp19_v0_28_adjoint_segment_arb.py`: `old_radius_and_identity` validates and replays the M14 predictor recurrence.

This note is a static source-and-frozen-artifact audit. It does not revise the frozen aggregates or certify the missing M15 radius.

# M14/M15 context from the related draft audit

**Reviewed:** 1 November 2026  
**Repository:** [`reggaesharkk/navier-stokes-bridge-audit`](https://github.com/reggaesharkk/navier-stokes-bridge-audit)  
**Related work:** [Draft PR #155](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/155), head commit `35bc96454b471bf37732c7ab216ee199055d80ac`  
**Disposition:** The M14/M15 objective-transfer bridge remains open.

## What the draft records report

The draft PR keeps the M14 dual-integral record and the M15 comparison separate, then adds a forced-radius replay and a weighted-remainder replay. Its duality-compatibility audit reports:

- **M14:** The v0.29 result in this package replays only the last three backward scalar-recurrence steps (239, 238, 237), with imported whole-segment strain and residual bounds. It does not enclose the complete M14 adjoint path.
- **M15 forced radius:** The draft reports `PASS_M15_FORCED_L2_RADIUS_ONLY`, with terminal L2 radius `10.559636070809868141657764813075`, over 240 half-steps in 12 shards. This is conditional on frozen M14 gradient and M15 residual majorants. It is a scalar L2 bound, not a modewise error vector or an objective-transfer estimate.
- **Weighted remainder:** The draft reports `NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS`. Its remainder upper is `164063087678950.088632165980`; the frozen signed-integral lower bound is `5758574435.605829673039071`. Subtracting the remainder upper from the signed lower leaves `-164057329104514.482802492940`, so this conservative bound set does not preserve the sign.
- **Breakdown:** The reported adjoint-defect integral is `240063.832492240296`, the support-corrected quadratic term is `114517700895378.757870383616`, and the terminal saved-adjoint boundary product is `49545386543507.498269542068`. The final 20 half-steps (220–239) contribute about 69.6% of the quadratic upper bound.
- **Semantic gate:** The later record reports `STOP_PILOT_NOT_AUTHORIZED`. The e219 record remains a specification rather than a certified modewise vector; terminal gradient compatibility is only aggregate L2, without a componentwise mismatch vector; and the global scalar Hessian estimate is not a viable closure route. The record says not to run the tail pilot until vector and localized-Hessian certificates exist.

These statuses have different meanings. `PASS_M15_FORCED_L2_RADIUS_ONLY` is a conditional radius result. `NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS` means the available remainder bounds fail to prove the needed sign; it does not show that the underlying finite-dimensional transfer is false. `STOP_PILOT_NOT_AUTHORIZED` means the next computation is blocked by missing certificate inputs.

## Evidence links

These immutable paths point to the draft PR's head commit. The v0.29.1 ZIP does not contain these later draft-branch files, and I did not independently execute their replay programs as part of this package review.

- [Duality audit summary](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/duality_compatibility_audit_20261002/README.md)
- [Machine-readable audit disposition](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/duality_compatibility_audit_20261002/audit.json)
- [M15 forced-radius record](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/duality_compatibility_audit_20261002/m15_forced_radius.json)
- [M15 weighted-remainder record](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/duality_compatibility_audit_20261002/m15_weighted_remainder.json)
- [Semantic-repair gate](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/semantic_repair_20261003/semantic_repair_gate.json)
- [Tail 220–239 pilot STOP record](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/joint_pairing_20261003/tail_220_239.json)

## Concrete next gate

Build a certified modewise error vector on an adjoint-relevant low-mode block, certify the terminal gradient mismatch componentwise, and derive a localized Hessian remainder small enough to preserve the signed margin. Keep the pilot stopped until those inputs exist. Replaying the same scalar bound or extending the finite cutoff alone will not address the dominant quadratic and terminal-boundary terms.

This is a finite-dimensional Galerkin audit only. It is not a continuum Navier–Stokes regularity proof, a blow-up exclusion, or a solution of the Millennium Problem.

## Separate earlier M14 VJP export found locally

I found the older `wp19-v0-27c1-M14.zip` export in my local research files. It is a 296.5 MiB archive with two arrays of shape `[241, 14147, 3]` and an `M14_arb_vjp_point.json` record. I checked the ZIP CRC and all three entries in its SHA-256 manifest; they pass. Ten local split parts also reassemble byte-for-byte to this ZIP.

The metadata describes the arrays as a binary64 reconstruction. It reports a 192-bit Arb-versus-FFT VJP comparison at one interior point and an Arb-versus-explicit-Fourier cross-check on 12 selected modes at that same point. Its own claim boundary says this is not an adjoint trajectory certificate and that no continuous Hermite residual, trajectory, or quadrature enclosure is supplied. I checked the archive and read its metadata; I did not recompute the Arb values. This export is not included in the v0.29.1 release package and does not close the M15 error-vector or full-path objective-transfer gap.

## Follow-up found in attack board v0.6

Keep the two M14 records separate. This package's M14 recurrence replay covers only three backward scalar steps (239, 238, 237), with imported segment bounds. PR #155 also records a 240-half-step signed quadrature for saved reconstructed fields. That quadrature is not a certified pairing along the true M15 error trajectory and does not supply a full-path objective transfer.

The later v0.6 attack-board file reports a targeted M15-support recomputation for steps 220–239. It says that shard's quadratic upper fell about 0.533%, and the full conservative remainder fell about 0.259%, to `163638394179339.980822081471920939981122`. The signed margin remains `-163632635604904.374992408432849939981122`; the reported improvement therefore does not close the sign.

I treat those improvement figures as **reported, not independently reproduced**. The PR's changed-file list does not include the claimed `targeted_m15_quadratic_replay.json`, and the PR description says no long GitHub Actions run was started. The committed active-support gate separately reports `FAIL_ACTIVE_SUPPORT_ROUTE_BLOCKED; NO_VECTOR_PROPAGATION`: the scalar radius is about 6.1 million times the approximate active-Hessian radius threshold, and the fixed aggregate gradient-mismatch bound already exceeds the signed-integral lower bound. It calls for a certified modewise error vector, componentwise terminal-gradient compatibility, and a useful localized Hessian bound before any pilot proceeds.

Sources: [attack board v0.6](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/Seven_Problem_Attack_Board_v0_6_2026-10-03.md), [active-support feasibility gate](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/active_support_20261003/active_support_feasibility_gate.json), and [semantic-repair gate](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/35bc96454b471bf37732c7ab216ee199055d80ac/results/wp19_v0_28/semantic_repair_20261003/semantic_repair_gate.json).

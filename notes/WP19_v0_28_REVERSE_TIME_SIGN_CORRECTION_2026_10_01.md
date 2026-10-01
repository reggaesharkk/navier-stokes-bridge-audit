# WP19 v0.28 reverse-time sign correction

**Status: strain-only scalar recurrence reproduced; conclusion is conditional on the archived continuous-segment bounds.**

This additive correction supersedes the sign interpretation in the earlier v0.28 backward-diffusion audit and its follow-up corrected-chain note. Those records remain unchanged as history. The claim that adding `nu * max(|k|^2) = 22.5` was required is withdrawn: the error radius is propagated from the terminal time toward decreasing forward time, and viscosity is contractive in that direction.

## Sign derivation

The archived producer defines the residual by

\[
r = \partial_t L - \operatorname{VJP}(u,L) - \nu\Lambda L.
\]

For the difference between an exact and approximate adjoint, the forward-time error equation has the form

\[
\partial_t e = \operatorname{VJP}(u,e)+\nu\Lambda e \pm r,
\]

where the sign of the forcing residual does not affect its norm bound. Set reverse time \(\tau=T-t\). Then

\[
\partial_\tau e=-\operatorname{VJP}(u,e)-\nu\Lambda e\mp r.
\]

In the \(L^2\) energy estimate, the transport part is skew, the Leray projection drops against divergence-free \(e\), the strain contribution is bounded by \(\|S(u)\|_{L^\infty,op}\), and

\[
\langle \Lambda e,e\rangle=\sum_k |k|^2|e_k|^2\ge 0.
\]

Therefore, in reverse time,

\[
D^+\|e\|_2/D\tau \le \|S(u)\|_{L^\infty,op}\|e\|_2+\|r\|_2.
\]

The negative viscous term can be dropped for an upper bound. The archived strain-only scalar recurrence is valid under its stated imported bounds. Adding `22.5` to the exponent coefficient remains a valid but looser upper recurrence, not a required correction.

## Recomputed recurrence

The fixed sequence is backward segments `239 -> 238 -> 237`, width `1/80000`, and decimal precision 90. The correction runner pins the segment, recurrence-report, A/B, prior audit, prior audit-source, and prior conservative-chain hashes. The separate verifier replays the recurrence using a Taylor expansion with an outward geometric tail bound. This is a second arithmetic implementation, **not** an independent derivation of the PDE estimate.

| Step | Strain upper \(L\) | Residual upper \(R\) | Recomputed strain-only radius | Archived outward radius | Optional `L+22.5` radius |
|---:|---:|---:|---:|---:|---:|
| 239 | 1758.617670280 | 771,029,886,342.810495 | 74,882,674,993.048618657819… | 74,882,674,993.048618657819…218 | 74,903,737,341.768086947968… |
| 238 | 1755.447052426 | 770,889,881,044.051112 | 76,553,735,316.602437456115… | 76,553,735,316.602437456115…384 | 76,596,803,403.200881441529… |
| 237 | 1752.285153301 | 724,222,211,753.270303 | 78,258,186,399.829279366902… | 78,258,186,399.829279366902…394 | 78,324,232,548.824619630746… |

For each step, the incoming radius is the preceding archived outward value. The replay is no larger than the archived value, and the optional `L+22.5` chain is larger. The archived strain-only radii are the governing values for this three-step scalar recurrence.

## Segment 237 A/B reconciliation

The A/B record pins the same baseline segment-237 SHA-256 and incoming radius, but it separately re-evaluates the strain, residual, and primal-radius upper bounds. Its displayed upper values are slightly larger than the segment record:

| Quantity | Segment 237 | A/B re-evaluation |
|---|---:|---:|
| strain upper | 1752.285153301 | 1752.285153303 |
| nominal residual upper | 53857205.702019 | 53857205.702021 |
| primal radius upper | 0.000055664765007 | 0.000055664765009 |

These are separate reported upper bounds; the A/B values are not substituted into the archived official chain. Its own old-formula recomputation is `78258186399.831235707571984…`, slightly above the archived outgoing value `78258186399.829279366902453…`, consistent with its larger displayed strain and residual bounds. The A/B artifact's structured-residual comparison remains diagnostic-only. It is a separate re-evaluation, not merely a display-rounding duplicate of the segment record.

## Provenance and reproduction

Run from the repository root:

```bash
python src/wp19_v0_28_reverse_time_sign_correction.py
python src/wp19_v0_28_verify_reverse_time_sign_correction.py
sha256sum -c results/wp19_v0_28/reverse_time_sign_correction_20261001/SHA256SUMS.txt
```

The result and manifest are under `results/wp19_v0_28/reverse_time_sign_correction_20261001/`. The package includes the two files that were missing from the earlier review bundle and listed in its inner manifests: `notes/WP19_CURRENT_STATUS_2026_09_30.md` and `.github/workflows/wp19_v0_28_backward_diffusion_audit.yml`. Inner manifests are repository-root-relative and should be verified from the repository root.

The archived predictor arrays, adjoint arrays, lower nodes, and primal segment JSON inputs needed to independently reconstruct the producer's segment bounds are not included in this correction package. The reported whole-segment strain and residual enclosures are therefore **not independently re-established here**; the recurrence conclusion is conditional on those archived bounds and their producer provenance.

## Claim boundary

This corrects one finite M14 backward-time scalar error-radius recurrence over three archived half-segments. It does not certify the full adjoint path, dual quadrature, nonlinear remainder, normalizer, signed-observable endpoint transfer, an all-cutoff statement, blow-up, or continuum Navier–Stokes regularity.

Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.

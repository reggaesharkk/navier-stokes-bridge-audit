# WP19 v0.28 step-237 signed reconstruction and uncertainty audit

**Date:** 2026-10-02  
**Scope:** finite M14, saved reconstructions, half-step 237/80000 to 238/80000.

## Reconstruction-only result

The exact-dyadic Arb pilot completed with frozen input hashes and emitted
`PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY`. Its signed integral enclosure is

`[93847.089937434118345, 93847.089937434118348]`.

The enclosure is strictly positive, with width (3\times10^{-15}). It applies
only to the saved cubic primal and adjoint reconstructions on this half-step.
It does not include true-path radii, the remaining time intervals, the nonlinear
remainder, endpoint Taylor remainder, or cutoff transfer.

The result artifact was produced by workflow run `36963878563`, artifact
`11208483589`, ZIP digest
`400ac4d41a68ec48f803fe0ff732964c1160581f78d1e46f1a202a48dfe5f7b0`.
The source formatter correction is in commit
`7ba21c0c01650f0dfc0cd9a1d4633cca583d9651`.

## Scalar uncertainty diagnostic

Using the full-path certificate's step-237 incoming/outgoing adjoint error
radii, independently checked residual upper bound, and (h=1/80000), the
coarse product bound is

`708453960530831310.810770686357212...`.

That is approximately (7.5490\times10^{12}) times the positive
reconstruction-only integral. Across all 240 intervals, the analogous sum is
approximately (7.0570\times10^{19}), about (5.1165\times10^8) times the
available v0.27 sign margin (137927743305.71941005).

These are conservative L2-product diagnostics. They do not show that sign
transfer fails; they show that the current scalar error radii cannot certify
it. Computing the same reconstruction-only central integral on all 240
intervals would not address this bottleneck.

## Decision and next gate

**Do not launch the 240-interval reconstruction-only quadrature.** The current
floating scout concerns the full cutoff difference, not this half-step
reconstruction integral, so it is not a like-for-like check.

The next useful gate is a goal-oriented signed uncertainty enclosure that keeps
time and Fourier/component structure when pairing path uncertainty with the
residual. It must be tested against the frozen step-237 case and compared with
the coarse bound above before any full-path scaling. The normalizer remains an
independent gate.

This remains finite M14 numerical certification work. It is not a continuum
regularity result.

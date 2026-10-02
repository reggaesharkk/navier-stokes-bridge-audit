# M14 dual-quadrature scale diagnostic

**Date:** 2026-10-02  
**Status:** arithmetic comparison only; no endpoint-sign transfer claim.

## Frozen quantities

The frozen reconstructed-path signed integral is enclosed by

`[5758574435.605829673039071, 5758574435.605829673039791]`.

Its interval width is `7.20e-13`, about `1.25031e-22` of the midpoint.

The prior terminal-endpoint correction record reports a combined known primal-tube upper allowance of `282300477.131407882477` (saved-adjoint center endpoint product, terminal mean-value allowance, and full-path interior tube bound).

The signed-integral midpoint is `20.3987414195` times that allowance. This ratio is a scale comparison only; it is **not** a certified sum, subtraction, or sign test.

## Why no combined conclusion follows yet

The quadrature freeze covers the signed pairing for the saved cubic primal and adjoint reconstructions. It does not enclose true-path radii or the continuous adjoint defect. The endpoint/tube allowance is a separate conditional record. Until the exact integration-by-parts identity, orientation, and missing adjoint-defect/nonlinear terms are independently reconciled, these numbers cannot be combined into an endpoint transfer bound.

## Next decisive gate

1. Derive the identity and sign from the frozen ODE conventions, independently of the producer's code.
2. Enclose the saved-adjoint Hermite defect pairing and nonlinear remainder over all 240 half-steps, using the already frozen primal/adjoint inputs.
3. Reconcile that full outward interval with the terminal endpoint record; only then test whether the finite M14 observable's sign survives.

This is the next high-value check because the reconstructed signed term is much larger than the prior endpoint/tube allowance. A pass would close a finite-path accounting gap only; it would not prove cutoff transfer or continuum regularity.

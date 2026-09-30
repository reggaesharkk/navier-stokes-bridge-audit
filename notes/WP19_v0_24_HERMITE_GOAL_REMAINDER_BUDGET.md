# WP19 v0.24 — Hermite-consistent goal-adjoint remainder budget

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Copyright:** © 2026 Prince Upadhyay. All Rights Reserved.  
**Status:** public floating verification stage after the successful v0.23 route-selection gate.

## Motivation

WP19 v0.23 independently rebuilt the fixed-F11 continuous adjoint with an analytic spectral VJP and backward RK4 integration. The route-selection gate passed on all four same-datum transitions, with maximum relative remainder about 1.27% and derivative/VJP checks below 1e-7 and 1e-8 respectively.

Before interval arithmetic is spent on the adjoint, v0.24 removes two remaining floating ambiguities from the scout architecture:

1. v0.23 paired the shell residual only at saved nodes, where the cubic-Hermite reconstruction derivative equals the saved RHS;
2. v0.23 used one RK4 step per original interval and trapezoid quadrature.

v0.24 instead uses the full reconstruction residual

`r(t) = f_{M+1}(E ubar_M(t)) - E d_t ubar_M(t)`

inside every segment, including the Hermite interpolation defect.

## Half-step adjoint and Simpson pairing

The adjoint is propagated backward with RK4 on a half-step grid, while the base state is evaluated from the exact cubic-Hermite interpolation of the saved predictor endpoint/RHS data.

The dual term is then integrated with Simpson's rule on every original segment:

`eta_M = integral <lambda(t), r(t)> dt`.

This gives an independent refinement of the v0.23 node-trapezoid result.

## Exact error decomposition target

With `x=E u_M`, `y=u_{M+1}`, and `e=y-x`, the higher-cutoff quadratic ODE gives

`e' = A(t)e + r - B(e,e)`

for the linearization `A(t)=Df_{M+1}(x(t))`.

If the adjoint satisfies `-lambda'=A(t)^*lambda` and `lambda(T)=J'(x(T))`, then

`<J'(x(T)),e(T)> = integral <lambda,r> dt - integral <lambda,B(e,e)> dt`.

The full observable difference is therefore

`J(y(T))-J(x(T)) = eta_M + dynamic_nonlinear_remainder + endpoint_Taylor_remainder`.

v0.24 measures each floating component separately.

## Candidate nonlinear remainder inequality

Using incompressibility and periodic integration by parts,

`|<lambda,B(e,e)>| = |<e, (e.grad)lambda>| <= ||grad lambda||_infty ||e||_2^2`.

The Fourier series gives the computable upper envelope

`||grad lambda||_infty <= sum_k |k| ||lambda_k||_2`.

v0.24 combines this with the predictor state difference plus a binary64 replay of the already certified whole-segment trajectory radii. This produces a design-level nonlinear-remainder budget.

## Decision gate

- If the Hermite/Simpson dual prediction remains close to the actual fixed-F11 cutoff change and the nonlinear-remainder budget is numerically usable, the next stage intervalizes the adjoint residual, dual pairing, state-difference envelope, and endpoint Taylor remainder.
- If the budget is too loose, the exact decomposition is retained but a sharper frequency-weighted remainder estimate is developed before interval execution.

## Claim boundary

All new v0.24 numerical values are floating scouts. The existing N11–N18 Arb trajectory certificates remain the rigorous finite results. No all-N persistence, continuum regularity, or singularity theorem is claimed.

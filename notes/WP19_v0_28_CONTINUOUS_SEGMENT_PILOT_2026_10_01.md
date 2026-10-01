# WP19 v0.28 continuous adjoint segment pilot

Base: merged v0.27c1, `eb58d058fbb39dcb5480690db070297e4e964780`.
No witness, K36, C500, signs, objective, or input trajectory is retuned.

## Frozen pilot

Only M14→15, forward half-step 239/80000→240/80000 (first backward segment).
Arb precision: 192 bits. Inputs: original N14 certificate and exported M14
adjoint, pinned by ZIP SHA-256 and internal predictor/report hashes.

Cubic Hermite polynomials are imported as exact binary64 dyadics, projected
onto the real divergence-free subspace, and convolved by carry-free
space/time polynomial multiplication. The degree-six residual is bounded
on the entire segment by the Bernstein convex hull, not by sampled nodes.
The original decimal predictor's validated radius is augmented by the
continuous discrepancy to the dyadic predictor. The archived conservative
primal recurrence is retained. Terminal gradient uncertainty is recomputed
about this centre; no nominal endpoint is treated as the true trajectory.

The nonlinear VJP uncertainty bound is
`(sqrt(sum |k|²)+(M+1)*sqrt(mode_count))*primal_radius*adjoint_norm`.
The backward logarithmic norm uses the symmetric strain envelope; viscosity
is dissipative in backward time. The independent Decimal checker propagates
one scalar error step. It does not independently recompute the residual.

## Execution and failure preservation

A separate explicit Fourier/time-coefficient check must pass first.
The actual segment computation has a 1800-second limit. Convolution timings,
failed logs, and any atomic segment output are uploaded with a manifest.
A timeout is an unfinished computation, never a certificate PASS.
No automatic 960-segment expansion is authorized by this workflow.

## Pending gates

Complete backward path, rigorous dual quadrature, nonlinear remainder,
normalizer control, and signed observable transfer inequality remain open.
This pilot is not a continuum or all-cutoff result.

## Executed failure and computational repair

Run `36813631740`, source commit `864fe3b61bb76615b379ae675323e63d4915aeae`,
exited 124 at the frozen 1800-second limit. All archive hashes and the
independent coefficient check passed. Input/terminal-gradient preparation
took 5.836 seconds; packing six base polynomials took 793.876 seconds.
Only three of nine convolution groups completed. No segment JSON exists and
no recurrence verifier ran. The failure log is preserved under
`results/wp19_v0_28/pilot_timeout_36813631740/`.

The repair changes coefficient storage only: initialize the highest nonzero
coefficient first and assign the remaining nonzero coefficients in descending
order. Omitted coefficients are exactly zero. The same coefficient balls,
18 multiplication expressions, dyadic imports, 192-bit precision, Bernstein
bound, witness, signs, and time segment remain fixed. This is not the proposed
nine-product algebra rewrite. The independent explicit sum self-check still
passes with the same displayed arithmetic radius. A 793000-degree two-entry
construction took 0.118 seconds locally; this is a packing diagnostic, not a
prediction of full-segment execution time.

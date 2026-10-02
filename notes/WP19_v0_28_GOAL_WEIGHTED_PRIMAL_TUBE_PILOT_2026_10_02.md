# WP19 v0.28 goal-weighted primal-tube pilot

**Date:** 2026-10-02  
**Scope:** frozen finite M14 reconstruction, half-step 237/80000 to 238/80000.

## Result

The goal-weighted primal-uncertainty pilot completed with frozen input hashes
and a 192-bit Arb enclosure. It integrates the linearized residual perturbation
by parts in time, replacing the coarse pointwise pairing with the saved adjoint
ODE defect; the quadratic perturbation is bounded separately.

- Adjoint ODE defect L2 supremum: `53857205.702017860930`
- Integrated first-order primal-tube term: `0.037474358743`
- Integrated quadratic remainder: `168.717904355502`
- Combined local interior contribution: `168.755378714245`
- Step-237 reconstruction-only signed integral:
  `[93847.089937434118345, 93847.089937434118348]`

After internal endpoint cancellation, the two interior uncertainty terms are
about `0.17982%` of this half-step's reconstruction-only signed integral.
The local endpoint products are large (`261036220.9454` and
`261082538.2023`); they must telescope through one continuous primal error
path and cannot be discarded or summed independently.

The result came from workflow `36965768209`, artifact
`11209358823`, ZIP digest
`fb62f3f389cec92e9c1bfa8daa80df670af99fd8a18cf76eb80a7c5687bf5d6f`.

## Next bounded gate

A 12-shard full-path computation is running as workflow `36966691176`: 240
half-steps, 20 per job, six jobs at a time, 150-minute job cap. It sums only
the reconstruction-based primal-tube linear and quadratic contributions,
checks exact 0..239 coverage, and keeps the terminal center endpoint product
separate. The workflow fails closed on missing shards or mismatched frozen
inputs.

Even a successful aggregate will not certify the terminal Taylor remainder,
terminal-gradient uncertainty, signed central integral over the whole path,
normalizer, cutoff transfer, or any continuum claim. Those remain separate
gates.

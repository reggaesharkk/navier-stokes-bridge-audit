# M14 reconstructed dual-integral full-path freeze

**Frozen:** 2026-10-02  
**Scope:** exact-dyadic signed dual quadrature for the saved M14 cubic reconstructions over all 240 half-steps.

## Result

- Status: `PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY`
- Coverage: steps 0–239, 12 shards × 20 steps
- Outward signed-integral enclosure: `[5758574435.605829673039071, 5758574435.605829673039791]`
- Aggregate JSON SHA-256: `8b3a7806e462786b887c635f1e6dbd323faadf8c5e0dedd42143969afebf75a3`
- Full machine-readable result: [aggregate.json](aggregate.json)

## Provenance

- Shard computation workflow run: [37002060801](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/37002060801), source commit `45fd0ae964f9a3f8df3222eb91de6ed96aa5b7b9`. All 12 shard jobs succeeded; the original aggregate job failed while decoding the shard files.
- Artifact-only recovery and validation: [37031754310](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/37031754310), successful. It reused those 12 completed shard artifacts, validated exact coverage and interval arithmetic, and uploaded the strict-JSON aggregate artifact.
- Recovered artifact ID: `11237961041`; GitHub artifact ZIP digest: `sha256:886a5f23e4ac6424944cc5207aa874bd51f435d818b6677b90940ede356ae826`.
- Frozen lower-path artifact: `11059294923`, ZIP SHA-256 `b0bb454fa320887c2b17dfd8a0bae916273253bb057ecff7acee3d6218234698`.
- Frozen adjoint-path artifact: `11121015458`, ZIP SHA-256 `330bb3e931fa8d45d1837c090b13a4a638fb54577cb26b8d8eaa2fe009303058`.
- The aggregate records hashes for the lower nodes/RHS/metadata, saved adjoint values/RHS/report, pilot source, and shard runner.

## Interpretation boundary

This certifies the signed integral only for the saved cubic reconstructions and imported frozen inputs. It does **not** enclose true primal or adjoint path radii, terminal-gradient/Taylor and nonlinear remainders, independent normalizer transfer, cutoff transfer, or continuum regularity.

## Next decision gate

Before combining this integral with endpoint or uncertainty budgets, independently derive and verify the signed integration-by-parts identity and its orientation. Then combine compatible outward intervals and test whether the corrected finite-observable sign survives the full uncertainty and normalizer budget. No sign-transfer claim is made by this freeze.

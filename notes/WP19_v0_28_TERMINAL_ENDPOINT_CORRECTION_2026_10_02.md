# WP19 v0.28 M14 terminal endpoint correction

**Date:** 2 October 2026  
**Scope:** Conditional finite-path correction for the reconstructed C500 objective at the terminal endpoint.

## Frozen inputs and provenance

- Full-path goal-weighted aggregation: run `36989510022`, artifact `11218692882`, digest `sha256:9166841d5174f9cf17acf94c583d3243c0bb8b46b3fd6506fd323bc531c3d27a`.
- Terminal shard (steps 220–239): artifact `11217521246`, digest `sha256:17875e9b111a9adae6f83c55f03e98a3dec48629a9ce9a3d58bde0b5abef752a`.
- Full-path adjoint-error record SHA-256: `c146232a0289dbd16204961501658c1ba1b0126efe7e83edecafa2bf3582089d`; it records 240 verified half-steps and terminal mismatch seed `73244978636.905585`.
- Terminal reconstructed-state radius from step 239: `0.000059241340007).
- Saved-adjoint center endpoint-product upper bound: `277957977.931533676582).

## Mean-value correction

Let `r_T` be the certified terminal state radius and `epsilon_T` the terminal gradient mismatch bound over that endpoint ball. The endpoint replacement error is bounded by

`|J(u(T))-J(ubar(T))-<lambda_saved(T),u(T)-ubar(T)>| <= epsilon_T * r_T.`

This single mean-value allowance covers both terminal-gradient uncertainty and the Taylor remainder; it does not assume a separately linearized endpoint.

Using outward Decimal arithmetic:

- `epsilon_T * r_T <= 4339130.683234376` (rounded upward to (10^{-9})).
- Corrected terminal endpoint allowance:
  `277957977.931533676582 + 4339130.683234376
  <= 282297108.614768052582`.
- Adding the full-path interior primal-tube contribution
  `3368.516639829895` gives a combined known primal-tube upper bound of
  `282300477.131407882477`.

## Status and boundary

The terminal gradient/Taylor allowance is now explicitly budgeted against the saved-adjoint center endpoint product. The result remains conditional on the frozen terminal mismatch enclosure and saved primal radius.

This does not certify the signed dual quadrature of the reconstructed path, any terms outside the stated integration-by-parts identity, the independent normalizer transfer, or continuum regularity. It is not a complete signed-C500 transfer certificate.

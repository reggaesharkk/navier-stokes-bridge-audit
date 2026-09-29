# WP19 v0.9 — Certified K36 Endpoint Sign Chambers

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** exact-rational endpoint perturbation certificate.  
**Scope:** the already validated N11, N12 and N13 same-rational-datum endpoint balls.  
**Not claimed:** N14 transfer, cutoff-uniform convergence, continuum regularity, or blowup.

## Result

For the C500 upper surrogate,

`G_C500 = [sum_K36 |n_g| - 9 sum_C500 tau_g n_g] / |z|^2`,

the only nonsmooth terms are the 36 K36 absolute values.

v0.9 certifies the sign of **all 36** K36 numerators inside each already validated endpoint uncertainty ball:

| cutoff | locked signs | weakest `|n_g| / Delta n_g` |
|---:|---:|---:|
| N11 | 36 / 36 | 3.10539895915 |
| N12 | 36 / 36 | 1.95714754698 |
| N13 | 36 / 36 | 5.27722246188 |

The calculation uses exact `Fraction` arithmetic for the canonical decimal endpoint, rational upper/lower square-root enclosures, and the already validated terminal L2 radius.

Thus every K36 absolute value is exactly a fixed signed numerator throughout each certified endpoint ball.

## Chamber structure

N12 and N13 have the **same** 36-sign chart.

N11 differs from N12 in exactly one key:

`((2,2,2),(2,5,8))`

which changes from positive at N11 to negative at N12.

So the N12->N13 endpoint transfer has no K36 endpoint kink at all.

## Prospective freeze

The N13 sign chart is frozen before any same-datum N14 endpoint certificate is generated.

Frozen sign-chart SHA-256:

`7cbb307c70aa14fabdc28ae07f0965716bf498e63c371b61e1b9bfd00611c7bd`

A future N14 transfer must use this exact chart without retuning.

## Consequence

Inside each certified endpoint ball,

`sum_K36 |n_g| = sum_K36 sigma_g^(N) n_g`.

The endpoint objective is therefore smooth on each validated ball. This complements the global kink-safe v0.8 quadratic envelope: v0.8 handles arbitrary sign changes; v0.9 proves that no such kink remains inside the current N11-N13 trajectory-error balls.

No all-N or continuum conclusion follows.

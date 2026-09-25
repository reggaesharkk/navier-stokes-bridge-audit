# WP17: Sparse Multiscale Ladder Adversary

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** sparse amplitude/phase adversarial search against the WP15 positive-stretching coefficient.  
**Scope:** instantaneous smooth periodic divergence-free Fourier fields, \(s=2\), fixed high-advector split \(K=2\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Motivation

WP16 showed that phase-only rearrangement on one evolved spectrum can raise

\[
C_\infty^{\rm stretch}
=
\frac{[N_2^{>K}]_+}{b_{\rm stretch}X_2}
\]

from about 1.038 to about 1.078.

A stronger adversary is allowed to change the **relative amplitudes between coherent scales** as well as their phases.

Use scaled copies of the exact sparse triad

\[
P=(1,0,0),\quad Q=(0,1,1),\quad R=(1,1,1)
\]

at integer scales \(m=1,\ldots,L\).

For each scale, keep the registered divergence-free polarizations and assign a real amplitude \(A_m>0\) plus an \(R\)-mode phase \(\theta_m\).

Global amplitude is irrelevant to \(C_\infty^{\rm stretch}\), so fix \(A_1=1\) and search only relative amplitudes and phases.

## 2. Scaling consistency

For one isolated scaled triad with fixed coefficient amplitude,

\[
G_m\sim m^2,
\qquad
X_{2,m}\sim m^4,
\qquad
\langle(\omega\cdot S\omega)_+\rangle_m\sim m^3,
\qquad
N_{2,m}\sim m^5.
\]

Therefore

\[
b_{{\rm stretch},m}
=
\frac{\langle(\omega\cdot S\omega)_+\rangle_m}{G_m}
\sim m,
\]

and

\[
b_{{\rm stretch},m}X_{2,m}\sim m^5,
\]

matching the \(H^2\) nonlinear transfer scale.

Thus the ladder is not rejected by dimensional mismatch.

## 3. Exact sparse objective

For each sparse field compute

\[
X_2=\sum_k |k|^4|a_k|^2,
\qquad
G=\sum_k |k|^2|a_k|^2.
\]

The high-advector transfer is computed exactly on occupied output modes:

\[
N_2^{>K}
=
-\Re
\sum_{k}
|k|^4\,
\overline{a_k}\cdot
P_k
\sum_{\substack{p+q=k\\|p|>K}}
i(q\cdot a_p)a_q.
\]

The physical-space coefficient is

\[
b_{\rm stretch}
=
\frac{\langle(\omega\cdot S\omega)_+\rangle}{G}.
\]

The adversarial quotient is

\[
\boxed{
C_\infty^{\rm stretch}
=
\frac{[N_2^{>K}]_+}{b_{\rm stretch}X_2}.
}
\]

## 4. Deterministic search

The companion audit searches ladder lengths \(L=2,\ldots,6\).

For each \(L\):

- fix \(A_1=1\);
- sample logarithmic relative amplitudes for \(A_2,\ldots,A_L\);
- sample phases \(\theta_1,\ldots,\theta_L\);
- retain the best state;
- refine it by local single-coordinate perturbations;
- recompute the best candidate on finer spatial grids.

The search grid is \(32^3\). Best states are independently checked at \(48^3\) and \(64^3\).

## 5. Falsification logic

If \(C_\infty^{\rm stretch}\) grows without apparent control as ladder length or amplitude contrast increases, that would motivate an explicit analytical counterexample family to the WP15 pointwise coefficient.

If the quotient remains bounded in this finite search, no theorem follows.

A finite optimizer can only raise the tested lower benchmark for any universal constant.

## 6. Interpretation barrier

The ladder is a specific sparse family, not all smooth fields. Search maxima are not global maxima. Positive stretching contains a pointwise positive part and therefore requires grid refinement.

No cutoff-independent constant, time-integral estimate, or global regularity result is claimed.

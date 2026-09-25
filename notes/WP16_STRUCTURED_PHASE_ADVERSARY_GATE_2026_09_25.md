# WP16: Structured Phase-Adversary Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** phase-only adversarial search against the WP15 positive-stretching coefficient.  
**Scope:** unforced periodic 3D Navier–Stokes Galerkin states, zero mean, \(s=2\), fixed high-advector split \(K=2\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Why phase-only search

WP15 showed that generic nonlinear-dominant random Fourier fields were less demanding than the registered structured phase-cascade trajectory for the candidate

\[
b_{\rm stretch}
=
\frac{\langle(\omega\cdot S\omega)_+\rangle}{G}.
\]

This suggests that hard cases may depend more on structured phase geometry than on spectral occupancy alone.

For a fixed Fourier shape multiplied by amplitude \(A\),

\[
N_2^{>K}\sim A^3,
\qquad
b_{\rm stretch}X_2\sim A^3,
\qquad
\nu Y_2\sim A^2.
\]

Therefore the large-amplitude pointwise quotient is

\[
\boxed{
C_\infty^{\rm stretch}
=
\frac{[N_2^{>K}]_+}
{b_{\rm stretch}X_2}
}
\]

whenever \(b_{\rm stretch}X_2>0\).

This quotient removes the arbitrary amplitude choice and tests the geometric candidate directly.

## 2. Phase-preserving adversarial family

Start from the registered structured initial state named combined_double_quarter_high.

For each canonical nonzero Fourier pair \(\pm k\) in its support, apply

\[
a_k \mapsto e^{i\phi_k}a_k,
\qquad
a_{-k}\mapsto e^{-i\phi_k}a_{-k}.
\]

This preserves:

- reality of the physical velocity field;
- divergence freedom;
- every modal magnitude \(|a_k|\);
- therefore \(E,G,X_2,Y_2,D\).

It changes only multi-mode phase geometry and hence the signed cubic transfers and physical-space stretching pattern.

## 3. Search objective

The primary objective is

\[
C_\infty^{\rm stretch}
=
\frac{[N_2^{>K}]_+}
{b_{\rm stretch}X_2}.
\]

Secondary diagnostics record

\[
\chi_{2,\rm high}
=
\frac{N_2^{>K}}{\sum |Z^{(2)}_{kpq}|}.
\]

A phase state with larger \(C_\infty^{\rm stretch}\) is more demanding for the WP15 candidate.

## 4. Deterministic search design

The companion module uses:

1. the exact structured support from the registered combined state;
2. deterministic random phase draws;
3. local coordinate perturbations around the best draw;
4. matched runs at \(N=4\) and \(N=7\);
5. fixed grid quadrature satisfying the repository aliasing checks.

No optimizer output is treated as globally optimal.

## 5. Falsification logic

If the search finds phase states with strongly increasing

\[
C_\infty^{\rm stretch},
\]

the WP15 coefficient becomes less plausible and may motivate an explicit analytical counterexample family.

If the quotient remains bounded over this finite adversarial search, the candidate survives another screen but remains unproved.

A finite optimization cannot establish a cutoff-independent universal constant.

## 6. Interpretation barrier

The search is over a finite-dimensional phase torus tied to one registered modal support. It does not cover all smooth fields.

The result may falsify proposed constants on the tested family or identify dangerous phase configurations. It cannot prove WP11 L2–L3 or global regularity.

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


## 7. Executed searches

### 7.1 Initial-support pilot

A fast phase-only search on the unevolved registered combined state reached

[
C_infty^{m stretch}approx0.06070.
]

The (N=4) and (N=7) values were identical to numerical precision because
the initial occupied support is the same inside both cutoffs and the static
(H^2) transfer pairs against occupied output modes.

This pilot therefore cannot reproduce the dangerous evolved WP14 state. It
shows that the cascade-generated support, not merely the initial eight
conjugate pairs, matters.

### 7.2 Evolved cascade-support adversary

The search was upgraded to the exact registered structured anchor

[
4	imes	ext{combined_double_quarter_high}
]

evolved by RK4 with (Delta t=0.0005) to

[
t=0.0035.
]

All canonical Fourier pairs with coefficient norm above (10^{-8}) were
eligible for phase rotation. Every modal magnitude and polarization was held
fixed.

For (N=7), the evolved anchor contained 709 active conjugate pairs. The
baseline large-amplitude quotient was

[
C_infty^{m stretch}=1.0381140504.
]

The best deterministic coordinate-search result was

[
oxed{
C_infty^{m stretch}=1.0778997042
}
]

for seed 20260925, a factor

[
1.0383249352
]

above the baseline.

A second seed reached

[
1.0722309805.
]

For (N=4), the evolved anchor contained 128 active conjugate pairs. Its
baseline quotient was zero; the two searches reached approximately

[
0.0687953
quad	ext{and}quad
0.0524743.
]

The best (N=7) state had

[
chi_{2,m high}approx0.26711
]

and

[
b_{m stretch}approx26.6581
]

in repository normalization.

The workflow artifact digest for the evolved-support search is

    sha256:4237705d4c3aa8a78b727142e557fdf16e30b344f28fd165d916bd17825ff69a

## 8. Consequence for the WP15 candidate

The evolved-support phase search demonstrates that phase geometry can make the
registered (N=7) spectrum measurably more demanding without changing its
modal magnitudes.

Because the viscous reserve is quadratic in a subsequent global amplitude
rescaling while both (N_2^{>K}) and (b_{m stretch}X_2) are cubic, any
all-smooth-data pointwise inequality of the WP15 form must accommodate the
large-amplitude limit of these finite states. Consequently the present search
raises the tested finite lower benchmark for a universal coefficient to at
least approximately

[
Cge1.07790
]

on this particular adversarial family.

This is **not** evidence that a finite universal (C) exists. The optimizer is
local, the support family is finite dimensional, the positive-stretching
functional is evaluated on a finite spatial grid, and only (N=4,7) are
compared.

No unbounded phase family was found.

The next unresolved question is therefore sharper: either construct a
support-expanding structured family for which
(C_infty^{m stretch}) grows without bound, or attack the independent
all-prefix time-integrability of (b_{m stretch}).

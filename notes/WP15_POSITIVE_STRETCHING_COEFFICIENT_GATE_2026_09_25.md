# WP15: Positive-Stretching Coefficient Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** analytical scaling survivor plus finite stress test.  
**Scope:** unforced periodic 3D Navier–Stokes, zero mean, \(\sigma=0\), \(s=2\), fixed high-advector threshold \(K=2\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Candidate exposed by WP14

WP14 found strong descriptive co-movement between the endpoint-normalized target

\[
\Gamma_{\rm req}
=
\frac{b_{\rm req}}{\|\omega\|_\infty}
\]

and the endpoint-normalized positive stretching factor

\[
g_{\rm stretch}
=
\frac{
\langle(\omega\cdot S\omega)_+\rangle
}{
\|\omega\|_\infty G
}.
\]

Multiplying by the endpoint scale eliminates \(\|\omega\|_\infty\) and exposes the noncircular candidate

\[
\boxed{
b_{\rm stretch}
=
\frac{
\langle(\omega\cdot S\omega)_+\rangle
}{
G
}.
}
\]

The pointwise L2-L3 candidate becomes

\[
\boxed{
N_2^{>K}
\le
\theta\nu Y_2
+
C\,b_{\rm stretch}\,X_2.
}
\]

No constant \(C\) is fitted or registered in advance.

## 2. Scaling check

Under fixed-energy concentration

\[
u_\lambda(x)=\lambda^{3/2}v(\lambda x),
\]

we have

\[
G\mapsto\lambda^2G.
\]

The local stretching density contains two vorticity factors and one velocity gradient, and its spatial mean/integral scales as

\[
\langle(\omega\cdot S\omega)_+\rangle
\mapsto
\lambda^{9/2}
\langle(\omega\cdot S\omega)_+\rangle.
\]

Therefore

\[
\boxed{
b_{\rm stretch}\mapsto\lambda^{5/2}b_{\rm stretch}.
}
\]

For \(s=2\),

\[
X_2\mapsto\lambda^4X_2,
\]

so

\[
b_{\rm stretch}X_2
\mapsto
\lambda^{13/2}
b_{\rm stretch}X_2,
\]

exactly matching the positive leading concentration scale of the signed \(H^2\) transfer.

Thus WP12/WP13 concentration scaling does not reject this candidate.

## 3. Unit constant already fails on the registered trajectory

The WP14 matched-state data contain a sampled point with

\[
\frac{b_{\rm req}}{b_{\rm stretch}}
\approx
1.023889
\]

for the combined perturbed \(N=7\), amplitude-4, \(\theta=0.25\) trajectory near \(t=0.0035\).

Therefore the special choice \(C=1\) is already false on that finite sample.

This does not reject a larger cutoff-independent constant.

## 4. Static stress-test quotient

For any smooth finite Galerkin field define

\[
C_{\rm req}^{\rm stretch}
=
\frac{
[N_2^{>K}-\theta\nu Y_2]_+
}{
b_{\rm stretch}X_2
}
\]

when \(b_{\rm stretch}X_2>0\).

If a universal pointwise estimate with finite \(C\) exists, then

\[
C_{\rm req}^{\rm stretch}\le C
\]

for every admissible field.

Finite random sampling cannot establish such a uniform bound. It can, however, falsify proposed constants and expose growth with cutoff or spectral family.

The companion audit therefore tests deterministic real divergence-free fields from:

- full Fourier balls;
- outer-half spectral shells;
- several deterministic seeds;
- cutoffs \(N=3,\dots,7\);
- a fixed amplitude chosen so that nonlinear transfer is not trivially buried by the viscous reserve.

## 5. Independent time-integral problem

Even if the pointwise estimate survives, WP11 L3 separately requires an independently controlled all-prefix integral of \(b_{\rm stretch}\).

The exact enstrophy identity uses the **signed** stretching

\[
\frac12 G'
=
\langle\omega\cdot S\omega\rangle-\nu D,
\]

not its positive part.

Therefore

\[
\langle(\omega\cdot S\omega)_+\rangle
\]

cannot simply be replaced by the signed quantity in the identity, and the energy identity alone does not supply

\[
\int_0^T b_{\rm stretch}(t)\,dt.
\]

This gate keeps pointwise domination and time-integrability as separate obligations.

## 6. Interpretation barrier

A bounded sampled \(C_{\rm req}^{\rm stretch}\) does not prove a cutoff-independent constant.

Growth in a deterministic finite family is evidence only until converted into an explicit analytical counterexample family.

If the candidate survives numerical stress, the next step is to seek either:

1. an analytical inequality for the pointwise bound; or
2. an explicit phase/spectral family making \(C_{\rm req}^{\rm stretch}\) unbounded.

No arbitrary-data global-regularity result is claimed.

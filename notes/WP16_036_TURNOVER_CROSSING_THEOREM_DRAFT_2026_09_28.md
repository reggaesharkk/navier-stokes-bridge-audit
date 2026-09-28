# WP16 finite-N11 K36 crossing theorem — pending certificate draft

**Prince Upadhyay — Independent Research**  
**Date:** 28 September 2026  
**Status:** theorem statement and proof skeleton only; endpoint certificate still pending

This note prepares the final mathematical statement that may be promoted **only**
after the validated-trajectory certificate closes. It does not itself assert a
new theorem.

The fixed inputs are already public:

- rationally interpreted 112-pair coefficient table:
  `results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json`
- witness SHA-256:
  `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- unchanged K36 orbit-key SHA-256:
  `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- exact initial-sign result SHA-256:
  `327378d1ba2978a66484f1266d984d240fdfdaf4c5785889a48eb187c9650885`
- viscosity `nu=0.1`
- Galerkin cutoff `N=11`
- endpoint time `T=0.003`.

## Exact initial field

Interpret every printed decimal coefficient in the fixed 112-pair witness as an
exact rational number. For each positive mode (k), apply the rational Leray
projection

[
a_k mapsto a_k-k,rac{kcdot a_k}{|k|^2},
]

and impose (a_{-k}=overline{a_k}), with zero mean. This gives a precisely
defined real, divergence-free trigonometric polynomial (u_0) in the finite
N11 Fourier-Galerkin space.

The existing exact checker proves

[
F(u_0)in
[645.8037741471,;645.8037741472],
]

hence (F(u_0)>0) exactly.

## Observable

For the fixed tracked output and fixed ordered source-orbit grouping, let
(z(u)) denote the complex normalizer and let

[
g_j(u)=operatorname{Im}!left(rac{w_j(u)}{z(u)}ight)
]

be the grouped signed contribution whenever (z(u)
eq0). Let

[
I(u)=sum_{jin K36}|g_j(u)|,
qquad
O(u)=sum_{j
otin K36}|g_j(u)|,
]

and define

[
F(u)=I(u)-9,O(u).
]

Because (I,Oge0),

[
F(u)ge0
iff
rac{I(u)}{I(u)+O(u)}ge0.9
]

whenever the denominator is nonzero. Thus a sign change of (F) is exactly a
crossing of the 90% K36 absolute-mass threshold.

## Finite Galerkin flow

Let (u(t)) be the unique solution of the unforced N11 Fourier-Galerkin ODE

[
partial_tu
+
P_{11}P[(ucdot
abla)u]
=

uDelta u,
qquad

u=0.1,
qquad
u(0)=u_0.
]

This is a finite-dimensional polynomial ODE. The certificate concerns only
this finite system.

## Theorem that the certificate is intended to establish

**Pending finite-N11 K36 crossing theorem.**  
Suppose a validated enclosure of the above N11 trajectory on
([0,0.003]) proves both

[
inf_{0le tle0.003}|z(u(t))|>0
]

and

[
F(u(0.003))<0.
]

Then there exists a time

[
t_*in(0,0.003)
]

for which

[
F(u(t_*))=0.
]

Equivalently, the fixed K36 absolute-mass fraction crosses the 90% threshold
along this explicit finite N11 trajectory.

### Proof

The exact initial checker gives (F(u(0))>0).

The normalizer bound excludes poles in every (g_j). The Galerkin trajectory
is continuous, each (w_j) and (z) is polynomial in the finite Fourier
coefficients, division by the nonzero normalizer is continuous, and absolute
value is continuous. Hence (F(u(t))) is continuous on the full interval.

If the validated endpoint enclosure gives (F(u(0.003))<0), the intermediate
value theorem gives at least one (t_*in(0,0.003)) with (F(u(t_*))=0).
The equivalence above identifies this with the 90% K36 mass crossing. QED.

The only unfinished mathematical work is therefore the validated trajectory,
normalizer and endpoint enclosure.

## Validated-path reduction

Let (v(t)) be the certificate's explicitly represented, real,
divergence-free comparison path with (v(0)=u_0), and let

[
r=
v_t+P_{11}P[(vcdot
abla)v]-
uDelta v.
]

For (e=u-v), the finite incompressible energy identity gives

[
rac{d}{dt}|e|_2
le
|
abla v|_{L^infty}|e|_2+|r|_2.
]

If segment (n), of width (h_n), has certified bounds

[
|
abla v|_{L^infty}le G_n,
qquad
|r|_2le R_n,
]

then an outward-rounded recurrence may use

[
arepsilon_{n+1}
le
e^{G_nh_n}arepsilon_n
+
egin{cases}
R_n,dfrac{e^{G_nh_n}-1}{G_n},&G_n>0,\\
R_nh_n,&G_n=0,
end{cases}
]

starting from the exact value (arepsilon_0=0).

The completed certificate must aggregate every continuous segment, not merely
sampled nodes.

## Endpoint observable enclosure

At the endpoint, the trajectory radius must be propagated into the grouped
observable. A sufficient bound uses a certified normalizer lower bound
(z_*>0) and, for every group,

[
|g_j(u)-g_j(v)|
le
rac{|w_j(u)-w_j(v)|}{z_*}
+
rac{|w_j(v)|,|z(u)-z(v)|}{z_*^2}.
]

Absolute value is 1-Lipschitz, so no fixed sign assumption for an individual
group is required. Summing the K36 and outside-group error bounds gives an
outward interval for (F(u(0.003))).

The final theorem gate is simply

[
operatorname{upper} F(u(0.003))<0.
]

## Publication gate

This draft may be relabeled as a proved finite theorem only when an independent
verifier confirms all of the following:

1. the witness, K36 and exact-anchor hashes match the fixed public inputs;
2. the certificate uses the declared protocol version and fixed predictor
   arrays;
3. all declared continuous-time segments are present exactly once;
4. every segment enclosure is tied to the fixed predictor/input hashes;
5. the accumulated trajectory-error radius is outward rounded from zero
   initial error;
6. the certified normalizer lower bound is strictly positive;
7. the certified endpoint interval has strictly negative upper endpoint;
8. the exact initial interval retains strictly positive lower endpoint;
9. the independent verifier returns PASS on the complete immutable package.

Until those gates close, the existing status remains: **exact positive initial
sign plus numerical negative endpoint, not a certified crossing**.

## Scope boundary

A successful certificate proves one explicit trajectory crossing in the finite
N11 Fourier-Galerkin ODE. It does **not** prove cutoff-uniform persistence,
continuum convergence, finite-time blowup, or global regularity for the
three-dimensional Navier-Stokes PDE.

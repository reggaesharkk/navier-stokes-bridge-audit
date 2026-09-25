# WP18: Isolated Scale-2 Triad Limit

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** exact algebraic reduction plus deterministic quadrature baseline.  
**Scope:** isolated scaled copy of the registered sparse triad, (s=2), high-advector split (K=2).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Why isolate the scale-2 triad

WP17 raised the refined finite adversarial benchmark for

[
C_infty^{m stretch}
=
rac{[N_2^{>K}]_+}{b_{m stretch}X_2}
]

to approximately (5.113), but the optimized ladders saturated the second-scale amplitude search boundary and suppressed most additional scales.

This gate isolates the exact (m=2) triad to determine the limiting baseline that the ladder is approaching.

## 2. Exact Fourier quantities

Use the registered sparse triad

[
P=(1,0,0),qquad
Q=(0,1,1),qquad
R=(1,1,1),
]

with the same polarizations as the helicity/phase gate.

At scale (m=2), amplitude (A), and (R)-mode phase (	heta), the field is supported on

[
pm2P,quad pm2Q,quad pm2R.
]

For the fixed high-advector threshold (K=2), direct sparse convolution gives

[
oxed{
N_2^{>2}(	heta)
=
-512A^3sin	heta.
}
]

The quadratic quantities are

[
oxed{
G=112A^2,
qquad
X_2=1024A^2.
}
]

## 3. Two-angle physical stretching reduction

Write

[
a=x,
qquad
b=y+z.
]

At unit scale (m=1), amplitude (A=1), the local stretching density reduces to

[
egin{aligned}
F_	heta(a,b)
=
2ig[
&-2sin a
+4sin b
+2sin	heta
-2sin(2a+	heta)
-2sin(2b+	heta)\
&-2sin(a-b+	heta)
+4sin(a+b+	heta)
-sin(a+2b+2	heta)\
&-2sin(a+3b+	heta)
+2sin(2a+b+2	heta)
+2sin(2a+2b+	heta)\
&-2sin(2a+3b+2	heta)
+sin(3a+2b+2	heta)
ig].
end{aligned}
]

Its torus average is the signed (H^1) stretching,

[
langle F_	hetaangle = 4sin	heta.
]

Define the normalized positive part

[
P_+(	heta)
=
rac{1}{(2pi)^2}
int_0^{2pi}int_0^{2pi}
max(F_	heta(a,b),0),da,db.
]

At scale (m=2), amplitude (A),

[
langle(omegacdot Somega)_+angle
=
8A^3P_+(	heta).
]

Hence

[
b_{m stretch}
=
rac{8A^3P_+(	heta)}{112A^2}
=
rac{A}{14}P_+(	heta).
]

The amplitude cancels from the adversarial quotient:

[
oxed{
C_infty(	heta)
=
rac{[-7sin	heta]_+}{P_+(	heta)}.
}
]

## 4. Deterministic quadrature protocol

The companion script performs:

1. exact sparse-convolution checks of
   [
   N_2^{>2}=-512A^3sin	heta;
   ]
2. deterministic uniform two-angle quadrature for (P_+(	heta));
3. a phase scan over (	hetain[-pi,0]);
4. independent refinement at
   [
   n=256,512,1024,2048,4096
   ]
   points per angular coordinate for the candidate maximum.

The positive-part integral is evaluated numerically; no exact closed form for
(P_+) is claimed.

## 5. Interpretation

If the isolated triad maximum lies below WP17, then the extra satellite scales
in the best ladder produce a genuine finite interaction correction.

If the isolated value matches WP17 after refinement, the apparent multiscale
advantage is only a finite-grid/search artifact.

Neither outcome proves a universal WP15 constant.

## 6. Scope barrier

This gate reduces one explicit family. It does not establish the global
supremum of (C_infty^{m stretch}) over all smooth fields and does not
address the independent time-integral requirement for (b_{m stretch}).

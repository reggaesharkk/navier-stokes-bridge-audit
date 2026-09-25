# WP11 draft PR #27: merge gate for audited infrastructure

**25 September 2026 — review record.** The mergeable unit is an exact
finite-Galerkin diagnostic, a proved fixed-band estimate at zero Gevrey
radius, and an explicitly open high-advector continuation target. This gate
does not claim a 3D Navier–Stokes regularity theorem.

## Review the statements before the code

1. Verify the sign and convolution convention against `src/evolve_galerkin.py`:
   `B_k=i P_k sum_{p+q=k}(q·a_p)a_q`, `a_dot=-B-ν|k|²a`, and
   `N=-Re<Au,AB>`. The p-restriction selects the **advector**, not an output
   shell. Reality partners and zero mean must be retained.
2. Check the symmetrized squared-symbol identity and the low-band lemma in
   `notes/WP11_ONE_SIDED_CROSS_FREQUENCY_PROOF_PACKAGE.md`. For fixed integer
   `K≥1`, `s>3/2`, and `σ=0`, the estimate

       |N_N^{≤K}| ≤ sK(1+K)^{s−1} sqrt(M_K) ||u_N||₂ X_N

   follows from skew transport, the mean-value inequality, and shifted
   Cauchy–Schwarz. Check `q=0` and `k=0` separately. Its coefficient may grow
   with K but must not depend on N. The positive-radius cross-check verifies
   the squared symbol only; it does not extend this low-band estimate.
3. Verify the algebra in `notes/WP11_THRESHOLD_FREE_PHASE_IDENTITY.md` by
   multiplying (R1) through by `|z|²+ε²`. For `ε>0`, the three terms are smooth
   for smooth finite-Galerkin trajectories, including `z=0`. At a zero the
   entire `Re(z_dot)` enters the activation remainder. The decomposition
   depends on ε; neither its terms nor an ε→0 limit have a favorable sign or
   cutoff-uniform bound from this identity.
4. Treat the active-triad magnitude sum as an ordered-convolution accounting
   quantity. The clean-output positivity lemma in
   `notes/WP11_ACTIVE_MASS_OBSTRUCTION.md` concerns one instantaneous output
   derivative. It does not show persistent growth or exclude a different
   phase-cancellation mechanism elsewhere in time or in another datum.
5. Preserve L2–L3 as an **unproved, one-sided all-prefix target**. The
   heat-flow construction rules out control of the particular absolute-tail
   coefficient by just L² and H¹ norms; it does not refute a signed estimate.
   Any future proof needs a coefficient controlled without using the desired
   high-norm bound, plus cutoff-independent continuation.

## Reproducible finite-cutoff checks

From repository root, run:

    python3 src/wp11_review_audit.py
    python3 src/wp11_phase_rate_audit.py --output /tmp/wp11_phase.json
    python3 src/wp11_scaling_audit.py --output /tmp/wp11_scaling.json
    python3 src/wp11_regularized_phase_audit.py

On 25 September 2026 the 16 review samples had maximum normalized
direct-versus-symmetrized discrepancy `5.09e−15`. The phase-rate run reported
worst finite-difference derivative errors `2.73e−9` (N=4) and `1.98e−10`
(N=7). The scaled image-lattice checks printed zero residual at λ=2; this
checks the indexed scaling operation, not a full larger Fourier ball or a
continuum limit. The eight regularized checks (two cutoffs, two times, two
ε values) had largest normalized reconstruction residual `1.64e−16` and
explicitly included zero-transfer triads. These tolerances are regression
evidence for finite algebra, not acceptance thresholds for a PDE proof.

## Merge decision

Keep PR #27 in draft until an independent reviewer checks steps 1–5 and the
four commands pass on the PR head. Once these are met, merge the package as
**finite-band lemma and diagnostic infrastructure**. Do not label the merged
package a proof of L2–L3, phase muting, global analyticity, or arbitrary-data
regularity. The short N=4/N=7 plots establish no universal ranking between
phase, covariance, and activation terms.

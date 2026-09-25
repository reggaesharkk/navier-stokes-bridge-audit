# Navier–Stokes bridge audit: finite Fourier diagnostics

## 24 September 2026 scope note

This project is maintained as an independent exploratory mathematical audit within the wider Reggae Shark Universe. Its finite-mode checks, counterexamples, and small-data estimate do not constitute an arbitrary-data global-regularity proof for the three-dimensional incompressible Navier–Stokes equations.

---

Prince Upadhyay, Independent Research · version 0.2 · 24 September 2026

This repository accompanies [REPORT.md](REPORT.md), a scoped audit of
ten finite Fourier Galerkin work packages for the **unforced, periodic**
three-dimensional Navier–Stokes equations. The most complete analytic
claim is the explicit, conservative **small-data** estimate in
[WP3_PROOF.md](WP3_PROOF.md). It is a version of a standard argument,
with no claim of priority or a proof for arbitrary initial data.

The original WP1–10 dynamic diagnostics evolve one fixed `N=4`, 257-mode Galerkin ODE
to `t=0.1` with viscosity `ν=0.1`. These finite-mode results do not
show infinite-resolution convergence, persistent cascades, blow-up,
or global regularity of arbitrary smooth data. Fourier shell labels
describe frequency support, not shapes in physical space.

Version 0.2 also includes [the Master Record supplement](MASTER_RECORD_SUPPLEMENT_2026_09_24.md),
with a separate aligned two-scale initial field evolved through `t=0.02`
at `N=4` and `N=5`. The supplementary phase, smooth-filter, strain,
and space-time commutator scripts and JSON outputs are in `src/`.
They verify finite-dimensional identities and expose an open proof gate;
they do not establish a cutoff-uniform regularity estimate.

## Files

| Path | Purpose |
| --- | --- |
| `REPORT.md` | Audited findings, numbers, exclusions, and limitations. |
| `WP3_PROOF.md` | Self-contained small-data estimate and proof audit. |
| `src/` | Python for WP1–10 and four supplemental diagnostics and JSON outputs. |
| `results/` | Output JSON recorded for the seeded calculations. |
| `notes/` | Individual package scope and derivations; WP8 correction included. |
| `MASTER_RECORD_SUPPLEMENT_2026_09_24.md` | Supplementary evidence register and open proof gate. |
| `CITATION.cff` | Software citation metadata for the v0.2 snapshot. |
| `LICENSE.md` | Reuse terms for code and research text. |

The released WP8 code uses `np.rint(np.fft.fftfreq(M)*M).astype(int)` to
avoid an integer-cast frequency indexing error on the 96³ grid.
Unexecuted long-time decay and alternative helicity proposals are not
part of this release.

## Reproduce selected results

Reference environment: Python 3.12.14, NumPy 2.3.5. From the repository
root, install the requirement and execute scripts from `src` so their
local imports resolve:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cd src
python small_data_bound.py > ../wp3_reproduced.json
python localized_energy_audit.py > ../wp8_reproduced.json
python localized_enstrophy_audit.py > ../wp9_reproduced.json
python verify_helical_cascade.py > ../wp10_reproduced.json
```

The matching stored outputs are `results/small_data_results.json`,
`results/localized_energy_results.json`,
`results/localized_enstrophy_results.json`, and
`results/helicity_results.json`. The other package runners and their
result filenames are described in `notes/`. Tiny floating-point
variations across hardware or NumPy builds are possible; compare the
reported identity errors and observables, not only raw JSON bytes.

Run the v0.2 companion diagnostics from the repository root after
installing the same requirements:

```bash
python src/phase_cascade_trajectory.py
python src/smooth_commutator_gate.py
python src/strain_alignment_trajectory.py
python src/spacetime_strain_commutator_gate.py
```

They write their corresponding `src/*results.json` files. The root
`MANIFEST.sha256` records an earlier release candidate; the checksums
for this source snapshot are in `MANIFEST_v0_2.sha256`.

## Subsequent exploratory work

[The cutoff space-time gate](notes/CUTOFF_SPACETIME_GATE_2026_09_24.md) extends the aligned two-scale trajectory to `N=4,5,6,7`, with independent RK4 step refinement and signed total stretching integrals. Its [script](src/cutoff_spacetime_gate.py) and [recorded output](src/cutoff_spacetime_results.json) are work after the frozen v0.2 release and Zenodo archive. The observed short-time stabilization for this field is not a cutoff-uniform estimate or an arbitrary-data regularity proof.

The [adversarial cutoff gate](notes/ADVERSARIAL_CUTOFF_GATE_2026_09_24.md) further varies amplitude, triad phase, and initial high-frequency enstrophy across the same short-time finite Galerkin cutoffs. Its [script](src/adversarial_cutoff_gate.py) and [results for N=4–6](src/adversarial_cutoff_results.json) and [selected N=7 cases](src/adversarial_cutoff_N7_results.json) are also post-v0.2 exploratory work. A strongly perturbed field exhibits larger cutoff gaps than the reference field; no continuum bound follows.

The [time-resolved inequality gate](notes/CANDIDATE_INEQUALITY_GATE_2026_09_24.md) records every sampled step of the existing stress cases and analytically rejects one proposed energy-only majorant by fixed-energy spatial concentration. Its [screening code](src/candidate_inequality_gate.py) and [N=4–6](src/candidate_inequality_results.json) and [selected N=7](src/candidate_inequality_N7_results.json) traces are post-v0.2 work. Rejecting this trial inequality does not settle the regularity question.

The [monomial majorant gate](notes/MONOMIAL_MAJORANT_GATE_2026_09_24.md) classifies energy-only enstrophy powers by fixed-energy concentration and time-integrability, and [screens the stored traces](src/monomial_majorant_gate.py). It identifies an obstruction for that specified family, not a regularity result. This is post-v0.2 work.

The [zero-helicity phase gate](notes/HELICITY_PHASE_GATE_2026_09_24.md) gives an exact six-mode witness with zero signed helicity in every occupied mode but phase-dependent enstrophy transfer. Its [script](src/helicity_phase_gate.py) and [outputs](src/helicity_phase_results.json) are post-v0.2 exploratory work and do not imply a long-time regularity mechanism.

The [local strain majorant gate](notes/LOCAL_STRAIN_MAJORANT_GATE_2026_09_24.md) reconstructs selected finite Galerkin fields and tests the exact pointwise eigenvalue envelope of vorticity stretching. Its [script](src/local_strain_majorant_gate.py) and [outputs](src/local_strain_majorant_results.json) are post-v0.2 diagnostics; the needed time-integrated coefficient remains unproved.

The [short-time signed alignment gate](notes/ALIGNMENT_DYNAMICS_GATE_2026_09_24.md) reconciles the local strain envelope with dense log-enstrophy traces at N=4–7. Its [script](src/alignment_dynamics_gate.py) and [results](src/alignment_dynamics_results.json) show increasing sampled T/M over the tested early interval; this finite-cutoff observation establishes no long-time or uniform bound. This is post-v0.2 work.

The [Riesz strain localization gate](notes/RIESZ_STRETCHING_GATE_2026_09_24.md) reconstructs strain from vorticity Fourier multipliers and measures where positive and negative stretching arise in selected early Galerkin snapshots. Its [script](src/riesz_stretching_gate.py) and [results](src/riesz_stretching_results.json) show concentration in a moving high-vorticity region, with measurable grid sensitivity. No time-integrated or continuum bound follows. This is post-v0.2 work.

The [pressure-Hessian gate](notes/PRESSURE_HESSIAN_GATE_2026_09_24.md) reconstructs the exact pressure Hessian for selected finite trigonometric snapshots, validates its Poisson source independently, and measures signed isotropic/deviatoric contributions to the instantaneous vortex-stretching response. Its [script](src/pressure_hessian_gate.py) and [results](src/pressure_hessian_results.json) show that pressure is not a universally negative contribution in these fields. The actual Galerkin local evolution has a projection residual; no regularity estimate follows. This is post-v0.2 work.

The [projection residual gate](notes/PROJECTION_RESIDUAL_GATE_2026_09_24.md) derives an exact four-term Galerkin stretching-rate budget, including omitted solenoidal nonlinear frequencies. Its [script](src/projection_residual_gate.py) and [results](src/projection_residual_results.json) audit all 24 stored scenario-cutoff cases at initial and endpoint states. The projection term vanishes in the first global enstrophy derivative but can be large in the stretching-rate derivative; no sign or cutoff-uniform bound is inferred. This is post-v0.2 work.

The [projection shell gate](notes/PROJECTION_SHELL_GATE_2026_09_24.md) decomposes the exact omitted-mode stretching-rate residual into unit radial bands for all 24 stored cases and samples four selected cases at five early times. Its [script](src/projection_shell_gate.py) and [results](src/projection_shell_results.json) locate the sampled negative residual near the cutoff. This gate also documents the correction that apparent positive initial residuals were roundoff-scale zeros. No sign theorem or cutoff-uniform estimate follows. This is post-v0.2 work.

The [retained-shell capacity gate](notes/BOUNDARY_CAPACITY_GATE_2026_09_24.md) compares upper retained-shell enstrophy with the omitted nonlinear response along four early trajectories and gives an exact initial-time counterexample to any predictor based only on the last two shell fields. Its [script](src/boundary_capacity_gate.py) and [results](src/boundary_capacity_results.json) are post-v0.2 exploratory work; lower-shell inputs can still carry essential information, and no continuum closure is inferred.


The [triadic coherence gate](notes/TRIADIC_COHERENCE_GATE_2026_09_24.md) decomposes the exact H1/enstrophy transfer into ordered Fourier-triad contributions, defining the absolute cubic envelope A_N and signed coherence chi_N=T_N/A_N. Its [sparse-triad script](src/triadic_coherence_gate.py), [24-case suite](src/triadic_coherence_suite.py), and recorded outputs are post-v0.2 diagnostics. The phase-sensitive coordinate passes the exact algebraic and finite-suite checks, but A_N itself remains an uncontrolled cubic quantity and no regularity estimate follows.

The [triadic envelope growth gate](notes/TRIADIC_ENVELOPE_GROWTH_GATE_2026_09_24.md) normalizes deterministic dense divergence-free fields to G=1 and measures A_N/G^(3/2), T_N/G^(3/2), and chi_N across N=2,...,7. Its [script](src/triadic_envelope_growth_gate.py) and [results](src/triadic_envelope_growth_results.json) show rising sampled absolute-envelope ratios together with strong random-phase cancellation. This finite seeded pattern is an obstruction diagnostic only; it proves neither asymptotic envelope growth nor a cancellation theorem.


The [triadic cancellation hierarchy gate](notes/TRIADIC_CANCELLATION_HIERARCHY_2026_09_24.md) inserts a mode-grouped envelope (B_N) between the raw ordered-triad envelope (A_N) and the signed transfer (T_N), giving the exact hierarchy (|T_N|\le B_N\le A_N). Its [script](src/triadic_cancellation_hierarchy_gate.py) and [results](src/triadic_cancellation_hierarchy_results.json) show that most sampled cancellation in dense (G=1) fields occurs among convolution pairs feeding the same output mode. The apparent finite-cutoff stability of (B_N/G^{3/2}) is not universal: since (B_N\ge|T_N|), the existing fixed-energy concentration obstruction still rules out an energy-only cutoff-uniform (B_N\lesssim G^{3/2}) bound.


The [local vorticity-direction depletion gate](notes/DIRECTION_DEPLETION_GATE_2026_09_24.md) adds Constantin-Fefferman-inspired physical-space diagnostics to the same N=4/N=7 tracked trajectories used by the triadic audit. Its [script](src/direction_depletion_gate.py) and [results](src/direction_depletion_results.json) measure vorticity-weighted local direction misalignment and the separation-direction determinant at three grid scales. The strongly perturbed N=7 trajectory develops the largest sampled small-scale direction defect, but these are finite-grid local proxies rather than the full Biot-Savart kernel or a regularity criterion.


The [direction-scaling obstruction gate](notes/DIRECTION_SCALING_OBSTRUCTION_2026_09_24.md) applies the fixed-energy concentration map to a normalized direction-slope candidate \(Q_{\rm dir}=L_{\rm dir}/\sqrt G\). Its [script](src/direction_scaling_obstruction_gate.py) and [results](src/direction_scaling_obstruction_results.json) show the exact scaling mismatch: \(Q_{\rm dir}\) is concentration-invariant while \(T/G^{3/2}\) grows like \(\lambda^{3/2}\). Therefore a \(G^{3/2}\) closure whose coefficient depends only on this normalized geometry is analytically obstructed. This does not contradict Constantin-Fefferman, whose hypothesis retains an absolute spatial coherence scale.


The [high-vorticity sampled coherence-radius gate](notes/HIGH_VORTICITY_COHERENCE_RADIUS_2026_09_24.md) restricts the vorticity-direction analysis to pairs satisfying the diagnostic threshold \(|\omega|\ge2\sqrt G\) at both endpoints. Its [script](src/high_vorticity_coherence_radius_gate.py) and [verified summary](src/high_vorticity_coherence_radius_verified_summary.json) show that the strongly perturbed \(N=7\) trajectory develops the smallest sampled absolute coherence radius and the largest high-vorticity pair population by \(t=0.015\). The moving threshold and finite grid make this a diagnostic proxy only, not the Constantin-Fefferman theorem or a continuum radius.


The [scale-competition gate](notes/SCALE_COMPETITION_GATE_2026_09_25.md) compares the sampled high-vorticity coherence-radius upper bound with the exact vorticity-gradient length \(\ell_\omega=\sqrt{G/D}\) on the tracked \(N=4\) and \(N=7\) trajectories. Its [script](src/scale_competition_gate.py) and [results](src/scale_competition_results.json) show that the perturbed \(N=7\) case closes most rapidly from \(\mathcal R_{\rm sample}\approx2.96\) to \(1.62\) while \(T/(\nu D)\) rises to about \(5.49\). The gate explicitly rejects interpreting this as a regularity margin: \(\rho_{\rm upper}^{\rm sample}\) is one-sided and \(\ell_\omega\) is not an analyticity radius.


The [Gevrey lower-bound gate v0.2](notes/GEVREY_LOWER_BOUND_GATE_2026_09_25.md) standardizes the weighted Fourier identity, separates persistence and positive-time smoothing schedules, and requires every eventual nonlinear majorant to be cutoff-uniform. Its [exact audit](src/smooth_gevrey_identity_audit.py) verifies the finite-Galerkin identity directly from the repository ODE, with [executed summary](src/smooth_gevrey_identity_verified_summary.json). The worst relative identity residual is \(4.14\times10^{-15}\). Descriptive \(N=4/N=7\) nonlinear-ratio separation is recorded but is not treated as a continuum estimate or analyticity lower bound.


The [Gevrey uniform majorant gate](notes/GEVREY_UNIFORM_MAJORANT_GATE_2026_09_25.md) proves, for zero-mean periodic fields with \(s>3/2\), the cutoff-independent estimate \(|\mathcal N_{\sigma,s}|\le C_s^G X_{\sigma,s}Y_{\sigma,s}^{1/2}\le C_s^G X_{\sigma,s}^{1/2}Y_{\sigma,s}\), with \(C_s^G=2c_sK_s\) independent of \(N\) and \(\sigma\). Its [verifier](src/gevrey_uniform_majorant_gate.py) and [executed summary](src/gevrey_uniform_majorant_verified_summary.json) confirm the repository trajectories satisfy the zero-mean/divergence/reality assumptions and remain far below the diagnostic lattice-constant reference. The gate also records the real obstruction: the resulting weighted energy inequality only gives immediate viscous absorption in a smallness regime \(C_s^G\sqrt X<\nu\), so cutoff-uniformity alone does not solve arbitrary-data regularity.


The [WP12 energy-level coefficient falsifier](notes/WP12_ENERGY_COEFFICIENT_FALSIFIER_2026_09_25.md) identifies \(\sqrt G\) as the unique monomial of the energy-level norms \(\mathcal E=\|u\|_2^2\) and \(G=\|\nabla u\|_2^2\) with the amplitude degree and Navier-Stokes scaling required of an L2-L3 coefficient. It then rejects the universal \(C\sqrt G\) high-advector coefficient analytically at \(s=2\) using the repository's positive-transfer triad, localization, and fixed-energy physical concentration. Its [finite falsifier](src/wp12_energy_coefficient_falsifier.py), [verified summary](src/wp12_energy_coefficient_verified_summary.json), and [Colab notebook](notebooks/WP12_energy_coefficient_colab.ipynb) retain the circular required coefficient only as a target for future noncircular geometric/frequency candidates.


The [WP13 endpoint-vorticity gate](notes/WP13_ENDPOINT_VORTICITY_GATE_2026_09_25.md) sharpens the WP12 concentration obstruction: for the fixed-energy family \(u_\lambda(x)=\lambda^{3/2}v(\lambda x)\), the required L2 coefficient scales like \(\lambda^{5/2}\), whereas \(\|\omega\|_{L^p}\sim\lambda^{5/2-3/p}\). Hence every finite-\(p\) magnitude-only coefficient \(C\|\omega\|_{L^p}\) is too weak on that family; the endpoint \(p=\infty\) is the first magnitude scale not rejected by this argument. The [finite endpoint diagnostic](src/wp13_endpoint_vorticity_gate.py) and [verified summary](src/wp13_endpoint_vorticity_verified_summary.json) compare the circular required coefficient with sampled \(L^4,L^8,L^\infty\) vorticity norms and a rigorous finite-Fourier endpoint envelope, while explicitly leaving the independent endpoint time-integral problem open.


The [WP14 endpoint-geometry coupling gate](notes/WP14_ENDPOINT_GEOMETRY_COUPLING_GATE_2026_09_25.md) matches the circular endpoint target \(\Gamma_{\rm req}=b_{\rm req}/\|\omega\|_{\infty,\mathrm{grid}}\) to dimensionless geometry on the same Galerkin states. It tests \(g_{\rm dir}=\ell_\omega L_{\max}\), endpoint-normalized positive stretching \(g_{\rm stretch}=\langle(\omega\cdot S\omega)_+\rangle/(\|\omega\|_{\infty,\mathrm{grid}}G)\), and exact high-advector \(H^2\) triadic coherence \(\chi_{2,\rm high}\). The [verified summary](src/wp14_endpoint_geometry_verified_summary.json) records strong descriptive co-movement of \(\Gamma_{\rm req}\) with \(g_{\rm dir}\) and \(g_{\rm stretch}\) on the aggressive \(N=7\) family, while explicitly not promoting correlation into an a priori estimate. The gate exposes the next noncircular candidate \(b_{\rm stretch}=\langle(\omega\cdot S\omega)_+\rangle/G\), whose domination and independent time-integral properties remain open.


The [WP15 positive-stretching coefficient gate](notes/WP15_POSITIVE_STRETCHING_COEFFICIENT_GATE_2026_09_25.md) tests the noncircular coefficient \(b_{\rm stretch}=\langle(\omega\cdot S\omega)_+\rangle/G\), which has exactly the concentration scaling required to multiply \(X_2\) in the signed \(H^2\) high-advector target. The [finite stress test](src/wp15_positive_stretching_gate.py) and [verified summary](src/wp15_positive_stretching_verified_summary.json) show that generic nonlinear-dominant random Fourier fields are less demanding than the registered structured phase-cascade trajectory: the random suite reached \(C_{\rm req}^{\rm stretch}\approx0.169\), while the structured \(N=7\) trajectory reached about \(1.024\). No cutoff-independent constant or independent time-integral estimate is proved.

## Status and rights

The source code and computations were checked for internal consistency;
the research has not been externally peer reviewed or accepted as a
novel PDE theorem. A public repository and a DOI identify a version;
neither certifies its mathematics. The Python code is licensed under
[MIT](LICENSES/MIT.txt); the research text is licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode).
See [LICENSE.md](LICENSE.md) for the file-level scope and attribution.

## Cite the archived version

For the v0.2 files, cite the version-specific Zenodo DOI:

Upadhyay, Prince (2026). *Navier–Stokes Bridge Audit: Finite Fourier
Diagnostics* (version 0.2) [software]. Zenodo.
[https://doi.org/10.5281/zenodo.22939984](https://doi.org/10.5281/zenodo.22939984).

The v0.1 DOI below identifies only the earlier snapshot.

Upadhyay, Prince (2026). *Navier–Stokes Bridge Audit: Finite Fourier
Diagnostics* (version 0.1) [software]. Zenodo.
[https://doi.org/10.5281/zenodo.22932635](https://doi.org/10.5281/zenodo.22932635).

The [v0.1 GitHub release](https://github.com/reggaesharkk/navier-stokes-bridge-audit/releases/tag/v0.1)
points to commit `f891356fb99c85ded244dd566d35438e52571792`. The Zenodo
record archives that 45-file snapshot. Later edits to `main` are not part
of the v0.1 archive.

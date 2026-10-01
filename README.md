Warning: truncated output (original token count: 14574)
Total output lines: 479

# Navier–Stokes bridge audit: finite Fourier diagnostics

> **Rights boundary — effective 1 October 2026:** New author-owned original material first published here from this date is **All Rights Reserved** by default. Earlier express licenses remain in force for the material they cover. Read [the rights policy](RIGHTS_POLICY_2026_10_01.md) and the [shared portfolio evidence standard](https://github.com/reggaesharkk/Reggae-shark-universe-/blob/main/PORTFOLIO_EVIDENCE_AND_RIGHTS_STANDARD_2026_10_01.md).

## 24 September 2026 scope note

This project is maintained as an independent exploratory mathematical audit within the wider Reggae Shark Universe. Its finite-mode checks, counterexamples, and small-data estimate do not constitute an arbitrary-data global-regularity proof for the three-dimensional incompressible Navier–Stokes equations.

---

Prince Upadhyay, Independent Research · version 0.2 · 24 September 2026

## 30 September 2026 — certified same-datum chain through N18

The fixed 112-pair rational datum is now computer-assisted certified at every finite Galerkin cutoff `N=11,...,18`, with no retuning between cutoffs. Each cutoff replays 120 whole-segment Arb residual/gradient enclosures, propagates a trajectory-error radius, certifies a strictly negative endpoint interval for `F=I-9O`, and verifies whole-path nonvanishing of the normalizer.

The N18 recovery reused 99 hash-validated completed segment certificates from the six-hour-limited run, computed only segments `099–119`, and reran the global endpoint and normalizer gates. The recovered N18 endpoint interval is `[-88.699660529,-84.159654865]`, with terminal error bound `0.000013774643` and whole-path normalizer lower bound `48860.59568947`.

See [WP19 v0.21](notes/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md) and its [machine record](results/wp19_bridge/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.json). This is a finite `N=11,...,18` theorem family for one frozen datum, not an all-cutoff or continuum Navier–Stokes theorem.


## 28 September 2026 finite-N11 validated crossing

The post-hoc 112-pair N11 turnover datum now has a completed computer-assisted certificate. All 120 whole-segment Arb residual/gradient enclosures were replayed from the preserved predictor arrays, the exact initial margin is positive, the normalizer remains bounded away from zero, and the endpoint interval is strictly negative. Therefore the fixed finite N11 Fourier-Galerkin trajectory has at least one K36 90% crossing on `(0,0.003)`.

Certified bounds include `F(0) in [645.8037741471,645.8037741472]`, uniform normalizer `>48990.29795521`, and `F(0.003) in [-54.748409847,-42.032667894]`. The certificate archive SHA-256 is `d29224e1dd4ad9f9454951415a3b080bc9f092839e24caaeddd056013785cfbe`.

See [the validated theorem note](notes/WP16_036_N11_VALIDATED_TURNOVER_2026_09_28.md). This theorem concerns one fixed, post-hoc finite N11 Galerkin trajectory only. It does not establish continuum Navier–Stokes regularity, blowup, or cutoff-uniform persistence.

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


The [WP13 endpoint-vorticity gate](notes/WP13_ENDPOINT_VORTICITY_GATE_2026_09_25.md) sharpens the WP12 concentration obstruction: for the fixed-energy family \(u_\lambda(x)=\lambda^{3/2}v(\lambda x)\), the required L2 coefficient scales like \(\lambda^{5/2}\), whereas \(\|\omega\|_{L^p}\sim\lambda^{5/2-3/p}\). Hence every finite-\(p\) magnitude-only coefficient \(C\|\omega\|_{L^p}\) is too weak on that family; the endpoint \(p=\infty\) is the first magnitude scale not rejected by this argument. The [finite endpoint diagnostic](src/wp13_endpoint_vorticity_gate.py) and [verified summary](src/wp13_endpoint_vorticity_verified_summary.json) compare the circular required coefficient with sampled \(L^4,L^8,L^\infty\) vorticity norms and a rigorous finite-Fourier endpoint envelope, while explicitly leaving t…4574 tokens truncated…onal datum now has validated K36 sign crossings for the finite N11 and N12 Fourier–Galerkin ODEs. The N12 run reuses the exact N11 datum, zero-padded in the new modes, with the same viscosity, observable, and endpoint. The post-audit run reports 120 independently rechecked Arb segments, initial F(0) in [645.8037741471,645.8037741472], endpoint F(0.003) in [-73.63322101,-70.396895629], and a whole-path normalizer lower bound of 49091.85228719.

See the [N11–N12 report](notes/N11_to_N12_Cutoff_Persistence_Report_v1.md), the [post-audit N12 receipt](results/wp16_n12_same_datum/post_audit_replay_20260929/n12_same_datum_certificate.json), and its [replay log](results/wp16_n12_same_datum/post_audit_replay_20260929/replay.log). The source and rerun instructions are in [next-work/n12_same_datum](next-work/n12_same_datum/README.md).

This rerun used the updated source, including the Arb decimal timestep and endpoint labels. The large predictor arrays remain separately downloadable from Drive; their hashes and the extraction command are documented with the source.

The results concern two specific finite-dimensional trajectories. They do not establish cutoff-uniform control, a continuum Navier–Stokes result, or blowup.


## WP16 N13 same-datum finite-cutoff certificate (29 September 2026)

The complete N13 package—including its source, predictor arrays, 120 segment enclosures, certificate, replay log, first-pass receipt, and per-file checksums—is attached to the [N13 GitHub pre-release](https://github.com/reggaesharkk/navier-stokes-bridge-audit/releases/tag/n13-same-datum-v1). The archive SHA-256 is `858eeec4a1cb323d23e91ffa9914af823a388a78ecc39c758abea3fcdec9ac5e`.

The fixed N13 Galerkin run passed 120/120 independent Arb comparisons. Its terminal error upper bound is 0.000012244529, endpoint interval is [-87.154087422, -83.563901281], and whole-path normalizer lower bound is 48869.38355689. The full N11–N13 comparison and scope limits are recorded in the [N11–N13 report](notes/N11_to_N13_Same_Datum_Cutoff_Report_2026_09_29.md).

These are finite-dimensional results for specified Galerkin systems. They do not establish cutoff-uniform control, a continuum Navier–Stokes result, or blowup.


## 29 September 2026 — WP19 consecutive-cutoff bridge program

WP19 starts a proof-oriented cutoff-comparison track built around the same fixed rational witness used in the N11-N13 Arb certificate family.

The analytic gate derives a lower-cutoff-only difference inequality for
`E_N(t)=||u_{N+1}(t)-u_N(t)||_2` with forcing

`h_N(t)=||(Π_{N+1}-Π_N)B(u_N,u_N)||_2`.

See [WP19 v0.1](notes/WP19_CONSECUTIVE_CUTOFF_BRIDGE_GATE_v0_1.md).

A separate [evidence map](notes/WP19_v0_2_EVIDENCE_MAP.md) records that the older prospective WP16 phase/K36 program continued through N17, while keeping those optimizer-derived N14-N17 states logically separate from the later zero-padded 112-pair same-datum Arb certificates at N11-N13. The N17 broad time gate passed, but its separately frozen mechanism gate failed or became unevaluable; that failure remains part of the record.

The first [WP19 scouting result](notes/WP19_v0_3_SCOUT_REPORT.md) evaluates the new-shell forcing on the saved N11 and N12 predictor paths. In node-sampled diagnostics, the forcing integral decreases from about `0.6925` for N11->N12 to `0.5239` for N12->N13. The crude Fourier-l1 strain majorant gives approximately 20x-overlarge endpoint error estimates, while a sampled physical-space symmetric-strain diagnostic reduces the gap to roughly 2x. This is **not a rigorous cutoff certificate**; it identifies the next proof bottleneck: a whole-segment rigorous enclosure of `||S(u_N)||_{L-infinity,op}`.

Compact outputs, provenance, and the SHA-256 values of the three Drive archive ZIPs are under [`results/wp19_bridge/`](results/wp19_bridge/). The scouting scripts are [`src/wp19_cutoff_bridge_diagnostic.py`](src/wp19_cutoff_bridge_diagnostic.py) and [`src/wp19_sampled_physical_strain.py`](src/wp19_sampled_physical_strain.py).

No WP19 result currently establishes cutoff-uniform convergence, a continuum theorem, Navier-Stokes blowup, or global regularity.


## 29 September 2026 — WP19 v0.4 one-sided K36 bridge

[WP19 v0.4](notes/WP19_v0_4_ONE_SIDED_K36_CUTOFF_BRIDGE.md) sharpens the cutoff question using an exact property of the frozen K36 observable. Every selected K36 orbit lies below norm 10 (maximum squared norm 93), so for any cutoff N>=10, adding modes supported strictly above N while holding the low coefficients fixed cannot increase F=I-9O. The direct high-shell effect is therefore one-sided favorable; only its dynamical backreaction on the existing low coefficients can threaten a negative sign.

The accompanying backreaction scout measures the low-mode forcing on the saved same-datum N11->N12 and N12->N13 trajectories. Its sampled recurrence values are about 0.3731 and 0.3230 versus observed low-mode endpoint drifts about 0.2256 and 0.2030. These are non-rigorous diagnostics. The next proof target is a rigorous whole-segment backreaction bound together with an orbit-aware low-mode endpoint perturbation certificate. No cutoff-uniform or continuum theorem is claimed.


## 29 September 2026 — WP19 v0.5 fixed finite coalition locality

The [v0.5 locality gate](notes/WP19_v0_5_FIXED_COALITION_LOCALITY.md) further reduces the K36 cutoff bridge to a fixed finite endpoint witness. A frozen N11-derived coalition of 200 outside-K36 orbit-pair groups defines an upper observable `U_C200` satisfying `F <= U_C200`. Together with all 36 K36 keys, the retained observable uses only 461 ordered K-channel source pairs and 569 Fourier modes, and this support no longer grows once the cutoff reaches N=11.

Without retuning the coalition, the saved same-datum endpoint diagnostics give `U_C200=-33.178421` at N11, `-44.220575` at N12, and `-46.113595` at N13. Those numerical values remain floating diagnostics pending interval re-evaluation; the finite-support inequality is algebraic.

The next open gate is no longer an all-low-mode L2 estimate. It is support-aware dynamical control of the fixed 569-mode set under backreaction from arbitrarily higher shells.


## 29 September 2026 — WP19 v0.6 dual-weighted residual bridge

The [v0.6 bridge](notes/WP19_v0_6_DUAL_WEIGHTED_RESIDUAL_BRIDGE.md) introduces a stronger endpoint upper surrogate and a goal-oriented cutoff-error diagnostic.

A frozen C500 outside coalition gives an exact algebraic upper bound `F <= G_C500` whenever the tracked normalizer is nonzero. The surrogate uses 1,048 ordered K-channel source pairs and 1,159 fixed Fourier modes; its support does not grow once the cutoff is at least 11.

The saved N11->N12 and N12->N13 predictor families were then used for a **non-rigorous discrete-adjoint scout**. Instead of bounding the entire cutoff error in L2 and multiplying by a global endpoint Lipschitz constant, the scout weights each projected cutoff defect by the sensitivity of the endpoint surrogate. The observed first-order defect sums are `-7.505923` and `-0.604941`, while the sums of the absolute step contributions are only `9.489442` and `6.198853`, compared with starting negative upper margins `47.816278` and `55.152798`.

This does not certify a cutoff bridge. It identifies a more promising rigorous target: interval-enclose the dual-weighted scalar residual and its second-order remainder. No cutoff-uniform or continuum Navier-Stokes theorem is claimed.


## 29 September 2026 — WP19 v0.7 C500 endpoint certificate

The [v0.7 certificate](notes/WP19_v0_7_C500_ENDPOINT_CERTIFICATE.md) upgrades the frozen C500 endpoint surrogate from a floating diagnostic to a rigorous endpoint functional on the already validated N11-N13 same-datum trajectories.

Using exact rational evaluation of the precisely defined decimal endpoint field together with the existing Arb-certified global coefficient-9 perturbation envelope, the true C500 upper-observable intervals are `[-54.174149219,-41.458407264]` at N11, `[-56.770960917,-53.534635536]` at N12, and `[-57.555599822,-53.965413679]` at N13. Every upper endpoint is strictly negative.

This does not predict an unseen cutoff. It validates the fixed endpoint objective that the v0.6 dual-weighted residual program will attempt to propagate across cutoffs. No continuum Navier-Stokes theorem is claimed.


## 29 September 2026 — WP19 v0.8 kink-safe quadratic dual bridge

The [v0.8 gate](notes/WP19_v0_8_KINK_SAFE_QUADRATIC_DUAL_BRIDGE.md) gives a global quadratic upper tangent for each K36 absolute-value term. It rewrites the endpoint bridge as one smooth signed scalar objective plus an explicit 36-group nonnegative quadratic correction, so a future interval adjoint proof need not assume that K36 group signs remain fixed.

On the existing N11->N12 and N12->N13 saved transitions, the quadratic corrections are about `0.7502` and `0.2681`. Combined with the v0.6 dual-weighted scout and the v0.7 certified base margins, large retrospective rigorization budgets remain. The dynamic terms are still floating diagnostics; no unseen cutoff or continuum theorem is certified.


## 29 September 2026 — WP19 v0.9 certified sign chambers

The [v0.9 certificate](notes/WP19_v0_9_CERTIFIED_K36_SIGN_CHAMBERS.md) proves that all 36 K36 numerator signs are fixed inside each of the already certified N11-N13 endpoint uncertainty balls. N12 and N13 share one sign chamber; N11 differs in one key. The N13 sign chart is frozen before any same-datum N14 endpoint result is generated.

## 29 September 2026 — WP19 v0.10 signed numerator certificate

The [v0.10 certificate](notes/WP19_v0_10_SIGNED_C500_NUMERATOR_CERTIFICATE.md) uses those sign locks and group-specific source perturbation bounds to certify the C500 signed numerator directly. The resulting certified C500 upper bounds are approximately `-44.8447`, `-54.4141`, and `-54.9610` at N11, N12, and N13.

This is still finite-cutoff endpoint work. The unresolved step is a rigorous dynamic next-cutoff bridge for the frozen signed numerator; no all-N or continuum theorem is claimed.


## 29 September 2026 — WP19 v0.11 fixed-Pi11 locality and prospective N14 scout

The [v0.11 note](notes/WP19_v0_11_FIXED_PI11_AND_PROSPECTIVE_N14.md) proves an exact endpoint-locality refinement: every frozen K36+C500 source orbit and every normalizer anchor is already contained in N11. Hence the frozen signed numerator, and `G_C500` whenever its normalizer is nonzero, depend only on the fixed projection `Pi_11 a` for every cutoff `M>=11`.

Using the N13 K36 numerator sign chart that was frozen prospectively in v0.9, an untouched same-rational-datum N14 predictor was generated with no retuning. Its floating endpoint has `F~-87.0883` and `G_C500~-52.8415`; a half-step comparison changes the endpoint state by about `6.12e-9` in L2, and the frozen N13 sign chart matches 36/36 at both step sizes.

The prospective N13->N14 dual-weighted signed-numerator scout finds `Delta G~+2.9190`: the C500 surrogate becomes less negative at N14, so the N11->N13 decreasing trend is not monotone. All 120 observed first-order step contributions are positive and the floating linearization remainder is about 0.04575% of the actual signed-numerator change.

These N14 values are predictor/scouting results, not a validated trajectory certificate. The existing Arb N14 whole-segment check remains to be run in an environment with `python-flint`. No all-N or continuum Navier-Stokes conclusion is claimed.


## 30 September 2026 — N14 validated and WP19 v0.12 recursive closure gate

The prospective same-rational-datum N14 Arb workflow completed with `PASS`: the 120 whole-segment 128-bit Arb enclosures give terminal trajectory-error upper bound `0.000012825905`, endpoint `F(T) in [-89.015834781,-85.160766265]`, and whole-path normalizer lower bound `48850.68586052`. The rigorous same-datum finite-cutoff chain is therefore N11, N12, N13, N14.

The [v0.12 recursive-closure note](notes/WP19_v0_12_RECURSIVE_CLOSURE_AND_REGULARITY_GATE.md) fixes the low projector at N11 and derives the exact high-to-low feedback forcing `Gamma_M`. A finite-dimensional energy estimate shows that convergence of this closure forcing in `L1_t L2_x` controls convergence of the fixed N11 projections, and hence controls the frozen signed C500 numerator through a finite Lipschitz constant.

The same note also proves why the observable cannot by itself be a regularity criterion: negative F/G occurs on smooth finite Fourier states, and the exact fixed-Pi11 identity makes G blind to arbitrary high-frequency additions. The correct next target is therefore a coupling estimate between shellwise closure increments and an independent high-frequency dissipation/continuation criterion. No all-N, continuum singularity, or global regularity theorem is claimed.


## 30 September 2026 — WP19 v0.13 fixed-output continuum closure

The [v0.13 note](notes/WP19_v0_13_FIXED_OUTPUT_CLOSURE_AND_WEAK_LIMIT.md) proves a cutoff-independent low-output bilinear estimate for `P11 B(a,b)` with explicit Fourier constant `sqrt(5574)`. It follows that, for any Leray-Hopf weak solution, spectral truncations of the high-frequency feedback converge in `L1_t L2_x` to the exact fixed-low closure forcing.

Because the frozen signed C500 numerator depends only on finitely many N11 coefficients, a future cutoff-uniform negative signed-numerator margin can pass along a standard Galerkin subsequence to a Leray-Hopf weak limit without requiring strong convergence of the entire state. This is a continuum observable passage, not a regularity theorem.

The remaining cutoff-transfer term is the state/backreaction drift; v0.13 isolates it from the direct new-shell closure contribution so the next proof gate can target it with the existing adjoint machinery.


## 30 September 2026 — N14 validated same-datum chain and WP19 v0.14

The prospective same-rational-datum N14 validation completed successfully. Using the unchanged 112-pair witness, frozen K36 keys, `nu=0.1`, `T=0.003`, and 120 whole-segment 128-bit Arb enclosures, the validated N14 endpoint is

`F(0.003) in [-89.015834781,-85.160766265]`

with terminal trajectory-error upper bound `0.000012825905` and whole-path normalizer lower bound `48850.68586052`. The rigorous same-datum finite-Galerkin chain is now **N11, N12, N13, N14**. See [the N14 validated result](notes/WP19_N14_VALIDATED_SAME_DATUM_RESULT_2026_09_30.md).

WP19 v0.14 then sharpens the recursive-closure analysis. In Fourier space, incompressibility gives `a_p dot q = a_p dot k` whenever `k=p+q`, so a fixed low-output interaction does not pay the high input derivative. Consequently,

`||P_11 B(a,b)||_2 <= sqrt(404724) ||a||_2 ||b||_2`

for divergence-free `a`, where independent Wolfram enumeration gives 5,574 nonzero N11 output modes and `sqrt(404724) ~= 636.179220031588`.

For one fixed Leray-Hopf solution this yields absolute summability of the direct high-shell-to-low closure increments. For consecutive distinct Galerkin solutions, the energy-only worst-case direct increment still has a leading `O(1/M)` rate, so summable cutoff transfer remains open. The remaining proof target is stronger shell decay plus recursive state/backreaction control. See [WP19 v0.14](notes/WP19_v0_14_DIVERGENCE_FREE_OUTPUT_FREQUENCY_CANCELLATION.md).

These results do not establish all-cutoff persistence, a continuum regularity theorem, finite-time blowup, or a solution of the three-dimensional Navier-Stokes Millennium problem.


## 30 September 2026 — WP19 v0.15 full-PDE residual scout

The [v0.15 scout](notes/WP19_v0_15_FULL_PDE_RESIDUAL_AND_APOSTERIORI_SCOUT.md) evaluates the full-PDE truncation residual `Q14 B(u14,u14)` on the 121 saved N14 predictor nodes. The finite N14 Galerkin path itself remains separately Arb-certified; the new residual calculation is floating scouting only.

The sampled residual has `L2_t H^-1 ~= 0.3313` and `L1_t H^-1 ~= 0.01669`, versus `L2_t L2 ~= 4.9704` and `L1_t H1 ~= 3.7718`. This large norm separation makes a negative-Sobolev a-posteriori strong-solution criterion a more plausible continuum-verification route than the older positive-residual-norm route.

No continuum strong-solution or regularity conclusion is claimed from v0.15.


## 30 September 2026 — WP19 v0.16 critical-space criterion no-go

The [v0.16 Arb gate](notes/WP19_v0_16_BGT_CRITICAL_SPACE_ARB_GATE.md) tests a published critical-space a-posteriori sufficient strong-existence criterion against the exact validated N14 cubic-Hermite reconstruction.

A 160-bit lower screen using one omitted mode and the first Hermite segment proves the criterion's left-hand side is already above one by an enormous margin: `log(LHS)>6.217838664529e12`. This is a rigorous no-go for that certification route, not evidence of singularity or nonexistence.

The continuum program now pivots to reconstruction-specific Fourier-linearized stability, retaining the actual modewise viscous damping and the known full-PDE truncation residual rather than collapsing the dynamics into a universal Gronwall constant.


## 30 September 2026 — WP19 v0.17-v0.18 fast tail stress test

The same frozen rational datum was extended in floating arithmetic through N18 with no retuning. N18 falsifies a simple monotone C500 trend, but the magnitude of consecutive cutoff corrections and the fixed-low recursive closure differences continue to shrink sharply.

The more relevant sampled closure-difference totals decrease from about `1.72e-2` (N14->15) to `9.07e-3`, `3.50e-3`, and `9.97e-4` (N17->18).

Rather than validate these cutoffs serially, N15-N18 whole-segment Arb checks were launched in parallel in workflow run `36669057015`. Until that matrix closes, N15-N18 remain scouting results and the rigorous same-datum chain remains N11-N14.

See [v0.17](notes/WP19_v0_17_SAME_DATUM_N15_N17_FAST_TAIL_SCOUT.md) and [v0.18](notes/WP19_v0_18_N18_STRESS_AND_PARALLEL_ARB.md).


## 30 September 2026 — WP19 v0.19-v0.20

[WP19 v0.19](notes/WP19_v0_19_BOUNDARY_ANNULUS_DIRECT_SHELL_THEOREM.md) uses exact Fourier support geometry to show that a new shell can feed a fixed P11 output only through the last 11 units of old radial support. The resulting direct consecutive-cutoff bound is O(M^-2) and absolutely summable by the Galerkin energy identity. This corrects the coarser v0.14 O(1/M) direct-term obstruction.

The only structural all-cutoff term left is recursive state/backreaction drift.

[WP19 v0.20](notes/WP19_v0_20_GOAL_ORIENTED_FIXED_F11_TAIL_ADJOINT_SCOUT.md) then tests a fixed low observable, F11(P11 u_M(T)), with a reconstruction-specific continuous adjoint. The dual-weighted shell corrections across N14->18 have magnitudes about `2.303, 0.433, 0.132, 0.0173`, and reproduce the actual fixed-F11 cutoff changes to within small observed first-order remainders.

This makes interval validation of the goal-oriented adjoint plus nonlinear remainder the current bridge target. No all-N or continuum theorem is claimed yet.


## 1 October 2026 — WP19 v0.28 correction

The separate backward-adjoint pilot omitted the reverse-time (+\nu |k|^2) contribution from its scalar error growth rate. The corrected audit supersedes those three outgoing radii for adjoint-error use; no segment continuation is certified from the earlier chain. See [the correction record](notes/WP19_v0_28_BACKWARD_DIFFUSION_RECURRENCE_CORRECTION_2026_10_01.md) and [current status addendum](notes/WP19_CURRENT_STATUS_2026_09_30.md). This does not alter the separate validated finite N11–N18 endpoint certificate.

The follow-up [corrected-chain certificate](notes/WP19_v0_28_CORRECTED_RECURRENCE_CHAIN_2026_10_01.md) independently recomputes the scalar error recurrence over the same three frozen M14 segments, including reverse diffusion. It is a limited recurrence result conditional on the pinned producer-supplied continuous-segment bounds; the full adjoint and signed-observable endpoint transfer remain open.

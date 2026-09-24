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

## Status and rights

The source code and computations were checked for internal consistency;
the research has not been externally peer reviewed or accepted as a
novel PDE theorem. A public repository and a DOI identify a version;
neither certifies its mathematics. The Python code is licensed under
[MIT](LICENSES/MIT.txt); the research text is licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode).
See [LICENSE.md](LICENSE.md) for the file-level scope and attribution.

## Cite the archived version

For the v0.2 files, cite the v0.2 Zenodo version DOI once Zenodo
processes the new GitHub release. The v0.1 DOI below identifies only
the earlier snapshot.

Upadhyay, Prince (2026). *Navier–Stokes Bridge Audit: Finite Fourier
Diagnostics* (version 0.1) [software]. Zenodo.
[https://doi.org/10.5281/zenodo.22932635](https://doi.org/10.5281/zenodo.22932635).

The [v0.1 GitHub release](https://github.com/reggaesharkk/navier-stokes-bridge-audit/releases/tag/v0.1)
points to commit `f891356fb99c85ded244dd566d35438e52571792`. The Zenodo
record archives that 45-file snapshot. Later edits to `main` are not part
of the v0.1 archive.

# Navier–Stokes bridge audit: finite Fourier diagnostics

Prince Upadhyay, Independent Research · release candidate 0.1 · 24 September 2026

This repository accompanies [REPORT.md](REPORT.md), a scoped audit of
ten finite Fourier Galerkin work packages for the **unforced, periodic**
three-dimensional Navier–Stokes equations. The most complete analytic
claim is the explicit, conservative **small-data** estimate in
[WP3_PROOF.md](WP3_PROOF.md). It is a version of a standard argument,
with no claim of priority or a proof for arbitrary initial data.

The dynamic diagnostics evolve one fixed `N=4`, 257-mode Galerkin ODE
to `t=0.1` with viscosity `ν=0.1`. These finite-mode results do not
show infinite-resolution convergence, persistent cascades, blow-up,
or global regularity of arbitrary smooth data. Fourier shell labels
describe frequency support, not shapes in physical space.

## Files

| Path | Purpose |
| --- | --- |
| `REPORT.md` | Audited findings, numbers, exclusions, and limitations. |
| `WP3_PROOF.md` | Self-contained small-data estimate and proof audit. |
| `src/` | Python for WP1–10. |
| `results/` | Output JSON recorded for the seeded calculations. |
| `notes/` | Individual package scope and derivations; WP8 correction included. |
| `CITATION.cff` | How to cite this release candidate; DOI can be added after deposit. |
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

## Status and rights

The source code and computations were checked for internal consistency;
the research has not been externally peer reviewed or accepted as a
novel PDE theorem. A public repository and a DOI identify a version;
neither certifies its mathematics. The Python code is licensed under
[MIT](LICENSES/MIT.txt); the research text is licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode).
See [LICENSE.md](LICENSE.md) for the file-level scope and attribution.

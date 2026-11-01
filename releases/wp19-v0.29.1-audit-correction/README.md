# WP19 v0.29.1 audit correction

**Author:** Prince Upadhyay · [ORCID 0009-0002-1170-4487](https://orcid.org/0009-0002-1170-4487)  
**Status:** finite-cutoff research audit; continuum regularity remains open  
**Rights:** all rights reserved; no reuse license is granted for these new materials.

## What this package does

This package reruns selected Python arithmetic and consistency checks over supplied finite-cutoff certificate JSON files for N=11 through N=18, supplied recurrence data, and supplied Fourier-mode data. It checks each cutoff certificate against the aggregate summary, checks interval bounds, replays selected decimal/rational calculations, and runs seven regression tests. The N14-to-N15 interval is a difference of signed-numerator intervals; it is not a difference of normalized G values.

The original Arb inputs and trajectories are not included. This package therefore checks the supplied certificate records but does not reproduce the Arb calculations that produced them. Hash strings for absent upstream data are recorded only as references and are not independently validated here.

## M14/M15 bridge checkpoint

The M14/M15 adjoint-path audit is a separate evidence lane from the N14/N15 endpoint-record comparison above. I do not treat the two labels or calculations as interchangeable.

- **M14:** The v0.29 replay recomputes the supplied 90-digit scalar recurrence for three backward steps (239, 238, 237), under both the conservative `L_strain + 22.5` bound and the reverse-time dissipative `L_strain` bound. The imported whole-segment strain and residual bounds are assumptions to this replay. It does not enclose the full M14 adjoint path.
- **Earlier M14 VJP export:** I found a separate older v0.27c1 archive locally. Its ZIP and three-entry SHA-256 manifest pass, but the metadata describes only a binary64 path reconstruction and one-point VJP cross-checks; it explicitly supplies no residual, trajectory, or quadrature enclosure. I did not rerun its Arb calculation, and the large archive is not included here. See [`M14_M15_DRAFT_PR155_CONTEXT.md`](M14_M15_DRAFT_PR155_CONTEXT.md) for the exact boundary.
- **M15:** The bundled `e219_certificate_spec.json` is a specification, not a certificate. The frozen record marks the joint-pairing pilot `STOP`; no validated modewise M15-versus-M14 error tube or certified full-path pairing is supplied. Therefore there is no signed endpoint-transfer closure from these files.
- **N14/N15:** The records in `data/frozen_v025b/` are supplied signed-numerator endpoint records. Their displayed difference is not a difference of normalized `G` values and does not close the M14/M15 adjoint bridge.

The user-provided executive report makes broader M14-to-M18 claims. The raw Arb inputs and trajectories needed to reproduce its transition table are not in this package, so this audit does not independently verify those claims.

## Later M14/M15 audit context

A related GitHub draft PR, [#155](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/155) (head commit `35bc96454b471bf37732c7ab216ee199055d80ac`, not merged), reports additional M14/M15 computations. Its M15 forced L2 radius is `10.559636070809868141657764813075` over 240 half-steps. The weighted-remainder record is `NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS`: its remainder upper is `164063087678950.088632165980`, against the frozen signed-integral lower bound `5758574435.605829673039071`. The semantic gate is `STOP_PILOT_NOT_AUTHORIZED`, and the active-support gate is `FAIL_ACTIVE_SUPPORT_ROUTE_BLOCKED; NO_VECTOR_PROPAGATION`.

Attack board v0.6 reports a targeted M15-support improvement on steps 220–239: about 0.533% on that shard and 0.259% for the full remainder. Its reported full remainder remains `163638394179339.980822081471920939981122`, leaving a negative signed margin of `-163632635604904.374992408432849939981122`. I treat this update as reported rather than independently verified because the claimed targeted output JSON is absent from the PR's changed-file list and the PR description says no long Actions run was started. These later draft values are not included in this ZIP or rerun by the v0.29.1 package. The M14 three-step recurrence in this package remains conditional on imported bounds; the PR's 240-step quadrature over saved reconstructions is a separate record. See [`M14_M15_DRAFT_PR155_CONTEXT.md`](M14_M15_DRAFT_PR155_CONTEXT.md) for the sources, limitations, and next gate.

## What it does not establish

- It does not prove global regularity or smoothness for the 3D Navier-Stokes equations.
- It does not prove an N-to-infinity limit or any statement covering every cutoff.
- It does not solve the Clay Millennium Problem.
- The Lean file contains elementary conditional arithmetic lemmas. Their hypotheses are assumptions; the theorems do not derive the research estimates or verify numerical certificates.
- The Python Lean scanner checks source text and declaration names only. It is not a Lean compiler. The Lake package now declares `NavierStokesWP19Bridge` as its default target and includes both the certificate module and a package-root import module, so a bare `lake build` compiles the actual Lean source. The GitHub workflow builds that library target explicitly and runs an axiom audit. An initial attempt to run the optional Nanoda checker ended with `invalid digit found in string` while parsing its exported environment, after the Lean build had succeeded; I removed that checker from the workflow and kept the compiler build and axiom audit.
- SHA-256 files provide byte-integrity checks only when compared with a trusted copy. They do not authenticate authorship or prevent someone from replacing both a file and its checksum.

## Run locally

From this directory, run the Python replay and tests:

```bash
python3 -B tools/check_ns_lean_axioms.py
python3 -B src/navier_stokes_v029_closure_suite.py
python3 -B -m unittest discover -s tests -v
python3 -B -O -m unittest discover -s tests -v
python3 -B -OO -m unittest discover -s tests -v
```

Build the Lean file with the pinned Lean 4.35.0 toolchain and Mathlib 4.35.0 dependency:

```bash
lake update
lake exe cache get
lake build
```

`lake update` creates `lake-manifest.json`, which pins the dependency revision for subsequent builds. The GitHub workflow performs the build and proof checks on every matching pull request and push.

## Contents

- `data/frozen_v025b/`: N=11..18 certificate JSON files and the aggregate summary.
- `data/frozen_v028/`: selected recurrence, interval, and modewise inputs used by the replay.
- `src/`: finite arithmetic and consistency replay.
- `tests/`: regression checks for the shipped computations and claim boundaries.
- `lean/`: conditional arithmetic lemmas; see the scope limits above.
- `results/wp19_v0_29/`: regenerated module outputs and the unauthenticated artifact checksum record.
- `tools/`: source-only Lean declaration scanner.

## Rights and attribution

Copyright (c) 2026 Prince Upadhyay. All rights reserved. No permission to reproduce, distribute, modify, or use these new release materials is granted by this notice. Contact the author for permission. This notice applies to the new v0.29.1 materials in this directory and does not alter licenses attached to pre-existing material elsewhere in the repository.

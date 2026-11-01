# Local verification record

Date: 2026-11-01

## Windows replay in this work environment

I reran the source-only Lean scan, the finite arithmetic replay, and the seven-test suite under normal Python mode, `-O`, and `-OO`. All five commands exited 0. The environment and console output are recorded in `run_logs/windows_*.txt` and `run_logs/windows_*.log`. This run used Python 3.12.14 on Windows 11 AMD64.

The separate PowerShell ZIP on D: contains six generated `.pyc` files that are not listed in its manifest and contains no captured run logs. Its listed files match, but its manifest does not cover the whole archive. I keep that ZIP separate from this cleaned review package.

## Ubuntu WSL2 replay found on D:

I found `NAVIER_STOKES_V029_UBUNTU_LOCAL_RUN_20261101.zip` on D:. Its ZIP integrity check passes, its manifest lists and matches all 33 non-manifest files, and the included environment log records the same input archive SHA-256 as the Downloads source ZIP. The captured environment is Python 3.14.4 on Linux WSL2 aarch64. The five run logs report the closure suite and source scan completed and seven tests passed under normal mode, `-O`, and `-OO`. I copied these logs into `run_logs/ubuntu_*` so they travel with this review package.

The Ubuntu `lean_check.log` was produced by the Python source scanner; it is not a Lean compiler run. The closure log's count of 12 Lean theorem declarations does not replace typechecking them.

## Lean build

A local `lake update` and `lake build` were attempted with the pinned Lean 4.35.0 toolchain and Mathlib v4.35.0 tag. Both stopped while fetching Mathlib because this environment could not resolve `github.com`; therefore I have no local Lean compiler result.

## GitHub Actions run 10 diagnostic

The Python replay job passed the archive checksum, package manifest, finite arithmetic replay, and all seven tests under normal mode, `-O`, and `-OO`. The Lean job completed `lake build NavierStokesWP19Bridge` successfully. The optional Nanoda step then failed with `invalid digit found in string` while parsing its exported environment, so the axiom audit was skipped. The workflow now omits Nanoda while retaining the explicit Lean library build and axiom audit. This recorded failure is a checker error; it is not a failed Lean compilation or a mathematical result.

## GitHub Actions run 12 diagnostic

The Python job and explicit Lean library build passed. The axiom-audit action reported zero declarations because it filters by the compiled module path; the theorem declarations were in `NavierStokesWP19BridgeCert`, outside the audited `NavierStokesWP19Bridge` root. Adding a forwarding root alone did not fix that mismatch. I moved the certificate source to `NavierStokesWP19Bridge.Cert`, made the root import it, and retained both prior module names as compatibility shims. The next GitHub run checks that module-path correction.

Input archive SHA-256: `aaf53b6f64fee6d0cf40ef70a7782bd6ad9b1e24d6662e08070c651cb56ef3fe`.

The upstream Arb raw inputs and trajectories are absent from this package. The package checks supplied finite-cutoff JSON fields and aggregate summaries; it does not reproduce the upstream Arb calculations or prove outward rounding. No all-cutoff limit or continuum Navier-Stokes regularity result is established.

## M14/M15 scope check

The M14 result in this package replays three backward scalar-recurrence steps (239, 238, 237) from imported whole-segment bounds. A separate older v0.27c1 M14 export found on the local drive has a passing ZIP and three-entry manifest; its metadata describes binary64 saved reconstructions and one-point VJP cross-checks, not a residual, trajectory, or quadrature enclosure. I did not recompute its Arb values, and that large archive is not included here.

The M15 joint-pairing record is `STOP`; it supplies no certified full-path M15-versus-M14 error tube or signed transfer. These records are separate from the N14/N15 signed-numerator endpoint check, which is not normalized `G`. The executive report's M14-to-M18 transition claims cannot be reproduced from the raw inputs included here because those inputs are absent.

## Related M14/M15 draft result

I also checked the public head of draft PR [#155](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/155), commit `35bc96454b471bf37732c7ab216ee199055d80ac`. Its records report a conditional M15 forced L2 radius of `10.559636070809868141657764813075` over 240 half-steps. Replaying the weighted remainder against that radius reports `NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS`: the remainder upper `164063087678950.088632165980` exceeds the signed-integral lower bound `5758574435.605829673039071`. The later semantic-repair record is `STOP_PILOT_NOT_AUTHORIZED`; the active-support gate is `FAIL_ACTIVE_SUPPORT_ROUTE_BLOCKED; NO_VECTOR_PROPAGATION`.

Attack board v0.6 later reports a targeted steps-220–239 recomputation that reduces the full remainder by about 0.259%, but the signed margin remains negative at `-163632635604904.374992408432849939981122`. I treat this improvement as reported, not independently verified: the claimed output JSON is absent from the PR's changed-file list and the PR says no long Actions run was started. The two M14 records are also distinct: this package replays three scalar recurrence steps, while the PR's 240-step quadrature covers saved reconstructions only.

This is a review of the public draft records, not a fresh execution of that branch's calculations. Its values are kept separate from the v0.29.1 package replay and do not constitute signed transfer closure. The detailed source paths and the next proof obligations are in `M14_M15_DRAFT_PR155_CONTEXT.md`.

## GitHub Actions run 41323635095 diagnostic

The Python job and Lean library build passed. The axiom-audit tool then reported `audited 0 declarations under NavierStokesWP19Bridge`: its root filter applies to compiled module names, not the Lean declaration namespace. The certificate module was named `NavierStokesWP19BridgeCert`, so a forwarding import at the root still left the audited module outside that prefix. I moved the certificate file to `lean/NavierStokesWP19Bridge/Cert.lean`; the new root imports that module, and compatibility import modules preserve the earlier paths. The next Actions run checks this correction.

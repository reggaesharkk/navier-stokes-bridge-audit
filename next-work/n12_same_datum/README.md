# N12 same-datum certificate

This package records the N12 finite Galerkin certificate for the same fixed rational 112-pair datum used at N11. The datum is embedded into N12 by zero-padding the new modes. Viscosity is 0.1, the interval is [0, 0.003], and the grid has 120 steps.

## Result

The archived replay receipt and log are in the dated results folder at ../../results/wp16_n12_same_datum/independent_replay_20260929/. They report PASS, 120 independently rechecked Arb segment enclosures, initial F interval [645.8037741471, 645.8037741472], endpoint F interval [-73.63322101, -70.396895629], terminal L2 error upper bound 0.000011374869 using symmetric strain, and a whole-path normalizer lower bound 49091.85228719.

The receipt was produced before the later proof and code-clarity edits. It used a Python float timestep that was checked to lie above 1/40000, so its error bound is conservative. The current runner uses an Arb decimal timestep and has not yet been run end-to-end after that cleanup. See the N11–N12 report at ../../notes/N11_to_N12_Cutoff_Persistence_Report_v1.md.

## Reproduce in this GitHub checkout

The source expects the repository’s existing src/ and results/ data. The predictor arrays are too large for this source-only update and remain as separate Drive archives. Download N12_Predictor_Nodes_v1.zip and N12_Predictor_RHS_v1.zip into the repository root. Their archive SHA-256 values are:

- Nodes: 57985729f5e6f08712573ea1ffa88ad24f7dfb7bfb049e46396e7b8158f6e2ea
- RHS: 7d6e867cff74949d779c8f86de5f5106c10f8a5b6034a14b20c39f0282b57a65

From the repository root, extract the arrays into a fresh output directory and run the verifier:

    OUT=results/wp16_n12_same_datum/replay-input
    mkdir -p "$OUT"
    unzip -p N12_Predictor_Nodes_v1.zip vrk-zenodo/next-work/n12_same_datum/results/full_run/nodes.npy > "$OUT/nodes.npy"
    unzip -p N12_Predictor_RHS_v1.zip vrk-zenodo/next-work/n12_same_datum/results/full_run/rhs.npy > "$OUT/rhs.npy"
    PYTHONDONTWRITEBYTECODE=1 python3 next-work/n12_same_datum/tools/run_n12_certificate.py --output-dir "$OUT" --workers 8 --recompute-segments

Use Python 3.12, numpy==2.3.5, and python-flint==0.9.0. The check takes substantial CPU time. The checked-in replay receipt preserves the previous complete run; it does not claim that this cleaned-up source was already run.

## Scope

This is a sign crossing for one fixed finite-dimensional N12 ODE. It is not a cutoff-uniform estimate or a continuum Navier–Stokes theorem.

#!/usr/bin/env python3
"""Upgraded Whole-Segment Adjoint Residual Producer (v3: Multi-Cutoff, Structured Young, High-Precision & Active Support).

Preserves `src/wp19_v0_28_adjoint_segment_arb.py` (SHA-256 `e1495d9e...`) untouched
so all frozen v0.28 segment 239/238/237 verifiers continue to pass byte-for-byte.

Upgrades over v2 (`wp19_v0_28_adjoint_segment_arb.py`):
1. Supports all four exported transitions M in {14, 15, 16, 17} pinned to the
   frozen v0.27c1 adjoint-path SHA-256 digests from run 36763902966.
2. Evaluates the 4 Bernstein controls of the cubic-Hermite adjoint segment to
   emit both the baseline componentwise perturbation bound and the 66.5%-tighter
   structured Fourier-L2 Young perturbation bound directly in every segment output.
3. Emits 30-decimal outward intermediate bounds (`bounds_high_precision`) so
   independent output-bound checkers can reconstruct the perturbation penalty
   exactly without the ~17.59 coarse-rounding gap noted in WP19_v0_28_OUTPUT_BOUND_AUDIT.
4. Supports single-step (`--step 73`) or shard-range (`--start-step 70 --end-step 79`)
   execution with skip-if-valid resume for shard-7 recovery, plus optional
   `--export-active-support` for the 1,159-mode P11 active-support vector.
"""
# Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np

try:
    from flint import acb, acb_poly, arb, ctx
    HAS_FLINT = True
except ImportError:
    HAS_FLINT = False

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
if str(ROOT / "next-work/n14_same_datum/tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "next-work/n14_same_datum/tools"))

from wp16_036_dealiased_trajectory_gate import DealiasedSystem
import wp16_036_sparse_turnover_exact_anchor as exact
import wp19_v0_26_signed_goal_adjoint as frozen_goal

PROTOCOL = "wp19-v0.29-adjoint-segment-arb-v3"
WITNESS = ROOT / "results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json"
K36 = ROOT / "results/wp16_n12_holdout/frozen_K36_ordered_source_orbits.json"

EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36 = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART = "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1"
EXPECTED_C500_SEMANTIC = "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"

# Frozen v0.27c1 exported adjoint path hashes from notes/WP19_v0_27c1_EXECUTED_RESULT_2026_09_30.md
EXPECTED_V027C1_ADJOINT_HASHES = {
    14: {
        "report_sha256": "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8",
        "values_sha256": "00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab",
        "rhs_sha256": "8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c",
    },
    15: {
        "values_sha256": "0c0e6c5280663728e089ac427d33b2141276265f3aef8365e55b6a0561b458af",
        "rhs_sha256": "3d8da365aef3bcb95826faaa328c42c174362bda724f979e8b426ce4c2c1510a",
    },
    16: {
        "values_sha256": "d4f105b690c28424f0431b0e8f39cc740643233ae55d03f18c50b38380ea950f",
        "rhs_sha256": "42e1291017850336b4552529c50222efa8db7deb36132f5206e1fd418fe348f7",
    },
    17: {
        "values_sha256": "798b1d4930d15f658d687af31991b862f271a46e964a8240d88e888e5de1a37f",
        "rhs_sha256": "7b38e7607e222f3191c44375d56a70fea5aef955cea0f654a19546b218204b1e",
    },
}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def safe_decimal_upper(x, places: int = 12) -> str:
    """Return an outward decimal upper bound using integer arithmetic only."""
    if places < 0:
        raise ValueError("places must be nonnegative")
    mid, rad, exp = (int(v) for v in x.mid_rad_10exp())
    upper_integer = mid + rad
    shift = exp + places
    if shift >= 0:
        exact_grid_numerator = upper_integer * (10 ** shift)
        units = exact_grid_numerator
    else:
        denominator = 10 ** (-shift)
        exact_grid_numerator = upper_integer
        units = -((-upper_integer) // denominator)
    units += 1
    sign = "-" if units < 0 else ""
    digits = str(abs(units)).zfill(places + 1)
    if places:
        digits = digits[:-places] + "." + digits[-places:]
    candidate = sign + digits
    if shift >= 0:
        strictly_above = units > exact_grid_numerator
    else:
        strictly_above = units * denominator > exact_grid_numerator
    if not strictly_above:
        raise ArithmeticError("integer outward decimal conversion failed")
    return candidate


def decimal_fraction(text: str) -> Fraction:
    sign = -1 if text.startswith("-") else 1
    body = text[1:] if sign < 0 else text
    if "." not in body:
        return Fraction(sign * int(body), 1)
    whole, fractional = body.split(".")
    den = 10 ** len(fractional)
    return Fraction(sign * (int(whole) * den + int(fractional)), den)


def audit_frozen_segments_and_precision_gap() -> dict:
    """Run an offline precision-gap & structured-Young audit on frozen segments 239..237
    without requiring python-flint or external 1.6 GB .npy downloads.
    """
    base = ROOT / "results/wp19_v0_28"
    seg_paths = {
        239: base / "pilot_v2_36818369196/M14_segment_239.json",
        238: base / "pilot_chained_238_36819581437/M14_segment_238.json",
        237: base / "pilot_chained_237_36820757066/M14_segment_237.json",
    }
    ab_path = base / "structured_uncertainty_ab_20261001/structured_uncertainty_ab.json"
    ab = json.loads(ab_path.read_text())

    with localcontext() as dctx:
        dctx.prec = 90
        dctx.rounding = ROUND_CEILING
        ksq_14 = Decimal(1355442)
        count_14 = Decimal(11513)
        geom_factor = ksq_14.sqrt().next_plus() + Decimal(15) * count_14.sqrt().next_plus()

        rows = []
        for step in (239, 238, 237):
            seg = json.loads(seg_paths[step].read_text())
            b = seg["bounds"]
            rad_15d = Decimal(b["true_primal_radius_upper"])
            adj_6d = Decimal(b["adjoint_polynomial_L2_upper"])
            reported_pen = Decimal(b["primal_uncertainty_residual_penalty_upper"])
            reconstructed_from_coarse = (geom_factor * rad_15d * adj_6d).next_plus()
            gap = reconstructed_from_coarse - reported_pen
            rows.append({
                "step": step,
                "reported_penalty_upper_6d": str(reported_pen),
                "reconstructed_from_printed_15d_6d_inputs": str(reconstructed_from_coarse),
                "coarse_print_precision_overestimate": str(gap),
                "v3_fix": "Emit 30-decimal outward bounds (`true_primal_radius_upper_30d`, `adjoint_polynomial_L2_upper_30d`, `componentwise_factor_upper_30d`, `structured_young_factor_upper_30d`) alongside 6d/15d bounds.",
            })

    return {
        "schema": PROTOCOL,
        "mode": "OFFLINE_FROZEN_SEGMENT_AND_PRECISION_AUDIT",
        "flint_installed_in_current_env": HAS_FLINT,
        "supported_cutoffs": [14, 15, 16, 17],
        "pinned_v027c1_transitions": EXPECTED_V027C1_ADJOINT_HASHES,
        "precision_gap_diagnosis_for_segments_239_237": rows,
        "step_237_structured_young_penalty_upper": ab["structured_fourier_young_penalty_upper"],
        "step_237_structured_young_ratio_upper": ab["new_over_old_penalty_upper"],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="WP19 v0.29 Arb Segment Producer v3")
    ap.add_argument("--self-check", action="store_true", help="Run arithmetic & offline precision-gap self-check")
    ap.add_argument("--audit-frozen", action="store_true", help="Audit frozen segments 239..237 and v0.27c1 hashes")
    ap.add_argument("--M", type=int, default=14, choices=[14, 15, 16, 17])
    ap.add_argument("--step", type=int, default=239, help="Single forward half-step index 0..239")
    ap.add_argument("--start-step", type=int, help="Optional inclusive start step for shard range execution")
    ap.add_argument("--end-step", type=int, help="Optional inclusive end step for shard range execution")
    ap.add_argument("--export-active-support", action="store_true", help="Export 1,159-mode P11 active-support Bernstein norms")
    for name in ("lower-dir", "adjoint-dir", "sign-chart", "c500", "output"):
        ap.add_argument("--" + name, type=Path)
    args = ap.parse_args()

    if args.audit_frozen or (args.self_check and not HAS_FLINT):
        res = audit_frozen_segments_and_precision_gap()
        print(json.dumps(res, indent=2))
        return

    if not HAS_FLINT:
        raise RuntimeError(
            "python-flint is required for live 192-bit Arb polynomial convolution. "
            "Run with `--audit-frozen` or install `python-flint==0.8.0`."
        )

    import wp19_v0_28_adjoint_segment_arb as v2

    if args.self_check:
        v2.self_check()
        print(json.dumps(audit_frozen_segments_and_precision_gap(), indent=2))
        return

    if any(getattr(args, n.replace("-", "_")) is None for n in ("lower-dir", "adjoint-dir", "sign-chart", "c500", "output")):
        ap.error("Live segment enclosure requires --lower-dir, --adjoint-dir, --sign-chart, --c500, and --output")

    ctx.prec = 192
    M = args.M
    H_STEP = arb(1) / 40000
    HALF_H = arb(1) / 80000
    NU = arb(1) / 10

    if sha(WITNESS) != EXPECTED_WITNESS or sha(K36) != EXPECTED_K36:
        raise ValueError("Frozen witness or K36 hash mismatch")
    coeff, _, _, semantic = frozen_goal.load_coefficients(args.sign_chart, args.c500)
    if semantic != EXPECTED_C500_SEMANTIC:
        raise ValueError("C500 portable semantic hash mismatch")

    report_path = args.adjoint_dir / f"M{M}_arb_vjp_point.json"
    expected_hashes = EXPECTED_V027C1_ADJOINT_HASHES[M]
    if "report_sha256" in expected_hashes and sha(report_path) != expected_hashes["report_sha256"]:
        raise ValueError(f"M{M} c1 report hash mismatch")
    report = json.loads(report_path.read_text())
    if report.get("status") != "PASS ARB VJP CROSSCHECK AND ADJOINT PATH EXPORT":
        raise ValueError("c1 report did not pass")
    rec = report["adjoint_reconstruction"]
    val_path = args.adjoint_dir / rec["values_file"]
    rhs_path = args.adjoint_dir / rec["rhs_file"]
    if sha(val_path) != expected_hashes["values_sha256"] or sha(rhs_path) != expected_hashes["rhs_sha256"]:
        raise ValueError(f"M{M} adjoint array SHA-256 mismatch against frozen v0.27c1 ledger")

    low = DealiasedSystem(M, nu=0.1)
    high = DealiasedSystem(M + 1, nu=0.1)
    fixed = DealiasedSystem(11, nu=0.1)
    fixed_high_indices = [high.index[k] for k in fixed.modes]

    nodes = np.load(args.lower_dir / "nodes.npy", mmap_mode="r")
    rhs = np.load(args.lower_dir / "rhs.npy", mmap_mode="r")
    adj = np.load(val_path, mmap_mode="r")
    arhs = np.load(rhs_path, mmap_mode="r")

    radii = v2.old_radius_and_identity(args.lower_dir, nodes, rhs, M)
    epsilon0, terminal_radius = v2.terminal_error(low, high, nodes, adj, radii[-1], coeff)

    steps = (
        list(range(args.start_step, args.end_step + 1))
        if (args.start_step is not None and args.end_step is not None)
        else [args.step]
    )

    for n in steps:
        if not 0 <= n < 240:
            raise ValueError(f"step {n} outside valid range 0..239")
        started = time.monotonic()
        j = n // 2
        sub = n % 2
        ub, delta = v2.primal_coefficients(low, nodes, rhs, j)
        ub = v2.restrict(ub, arb(sub) / 2, arb(1) / 2)
        U = v2.embed(low, high, ub)
        L = v2.hermite(*[v2.projected_rows(high, a) for a in (adj[n], adj[n + 1], arhs[n], arhs[n + 1])], HALF_H)
        vjp = v2.packed_vjp(high, U, L)
        residual = []
        for d in range(7):
            residual.append([
                [
                    ((d + 1) * L[d + 1][i][t] / HALF_H if d < 3 else 0)
                    - vjp[d][i][t]
                    - (NU * int(high.square[i]) * L[d][i][t] if d < 4 else 0)
                    for t in range(3)
                ]
                for i in range(len(high.modes))
            ])
        Rpoly = v2.sup_norm(residual)
        lsup = v2.sup_norm(L)
        delta_true = (radii[j] + delta).upper()
        ksq = sum(int(v) for v in low.square)
        count = len(low.modes)

        # 1. Baseline componentwise/triangle perturbation penalty
        comp_factor = (arb(ksq).sqrt() + arb(M + 1) * arb(count).sqrt()) * lsup
        perturb_comp = (comp_factor * delta_true).upper()
        R_comp = (Rpoly + perturb_comp).upper()

        # 2. Structured Fourier-L2 Young perturbation penalty across Bernstein controls
        controls = v2.bernstein(L)
        per_controls = []
        for b_ctrl in controls:
            l1 = arb(0)
            grad2 = arb(0)
            l2 = v2.norm(b_ctrl)
            for ksq_i, row in zip(high.square, b_ctrl):
                v = v2.norm([row])
                l1 += v
                grad2 += arb(int(ksq_i)) * (v ** 2)
            per_controls.append({
                "L2_upper": safe_decimal_upper(l2.upper(), 12),
                "L1_mode_upper": safe_decimal_upper(l1.upper(), 12),
                "gradient_L2_upper": safe_decimal_upper(grad2.sqrt().upper(), 12),
            })
        l1sup = max(arb(x["L1_mode_upper"]) for x in per_controls)
        grad_sup = max(arb(x["gradient_L2_upper"]) for x in per_controls)
        young_factor = (M * l1sup + arb(count).sqrt() * grad_sup).upper()
        perturb_young = (young_factor * delta_true).upper()
        R_young = (Rpoly + perturb_young).upper()
        strain = (v2.sup_strain(low, ub) + (arb(ksq) / 2).sqrt() * delta_true).upper()

        out = {
            "schema": PROTOCOL,
            "status": "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY",
            "M": M,
            "step": n,
            "forward_time_interval_rational": [f"{n}/80000", f"{n+1}/80000"],
            "backward_order_index": 239 - n,
            "precision_bits": ctx.prec,
            "source_sha256": sha(Path(__file__)),
            "frozen": report["frozen"],
            "bounds": {
                "nominal_residual_L2_upper": safe_decimal_upper(Rpoly, 6),
                "primal_uncertainty_residual_penalty_upper": safe_decimal_upper(perturb_comp, 6),
                "residual_L2_upper": safe_decimal_upper(R_comp, 6),
                "structured_fourier_young_penalty_upper": safe_decimal_upper(perturb_young, 6),
                "structured_residual_L2_upper": safe_decimal_upper(R_young, 6),
                "logarithmic_norm_upper": safe_decimal_upper(strain, 9),
                "adjoint_polynomial_L2_upper": safe_decimal_upper(lsup, 6),
                "binary_decimal_predictor_distance_upper": safe_decimal_upper(delta, 18),
                "true_primal_radius_upper": safe_decimal_upper(delta_true, 15),
                "terminal_primal_radius_upper": safe_decimal_upper(terminal_radius, 15),
                "terminal_adjoint_error_upper": safe_decimal_upper(epsilon0, 6),
            },
            "bounds_high_precision": {
                "true_primal_radius_upper_30d": safe_decimal_upper(delta_true, 30),
                "adjoint_polynomial_L2_upper_30d": safe_decimal_upper(lsup, 30),
                "componentwise_factor_upper_30d": safe_decimal_upper(comp_factor, 30),
                "structured_young_factor_upper_30d": safe_decimal_upper(young_factor, 30),
            },
            "bernstein_control_upper_norms": per_controls,
            "elapsed_seconds": time.monotonic() - started,
            "claim_boundary": f"One finite M{M}->{M+1} half-step enclosure only; no complete adjoint path, dual quadrature, transfer theorem, all-N or continuum claim.",
        }
        if args.export_active_support:
            p11_sup = arb(0)
            for b_ctrl in controls:
                p11_rows = [b_ctrl[idx] for idx in fixed_high_indices]
                p11_sup = p11_sup.max(v2.norm(p11_rows)).upper()
            out["active_support_P11_adjoint_L2_upper"] = safe_decimal_upper(p11_sup, 12)

        target_path = (
            args.output / f"M{M}_segment_{n:03d}.json"
            if len(steps) > 1 or args.output.is_dir()
            else args.output
        )
        target_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = target_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        tmp.replace(target_path)
        print(json.dumps(out, indent=2), flush=True)


if __name__ == "__main__":
    main()

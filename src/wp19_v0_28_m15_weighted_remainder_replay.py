#!/usr/bin/env python3
"""Recompute M15 duality remainders from frozen per-step artifacts.

This applies the M15 forced L2 radius to the saved adjoint-defect rows and
enlarges the convolution support factor from the M14 mode count to M15.
All decimal inputs are outward bounds; arithmetic is exact rational apart
from square roots, which are rounded upward by integer arithmetic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

H = Fraction(1, 80_000)
SCHEMA = "wp19-v0.28-m15-weighted-remainder-v1"
DELTA_PRINT_PLACES = 15
QUADRATIC_PRINT_PLACES = 12


def load_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.endswith("\\n"):
        raw = raw[:-2]
    return json.loads(raw)


def dec_fraction(text: str) -> Fraction:
    return Fraction(Decimal(text))


def ceil_decimal(value: Fraction, places: int = 12) -> str:
    scale = 10**places
    units = (value.numerator * scale + value.denominator - 1) // value.denominator
    digits = str(units).zfill(places + 1)
    return digits[:-places] + "." + digits[-places:]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def modes_in_ball(n: int) -> int:
    return sum(
        x*x + y*y + z*z <= n*n
        for x in range(-n, n+1)
        for y in range(-n, n+1)
        for z in range(-n, n+1)
    )


def sqrt_upper_ratio(numerator: int, denominator: int, places: int = 30) -> Fraction:
    scale = 10**places
    target = numerator * scale * scale
    q = (target + denominator - 1) // denominator
    units = math.isqrt(q)
    if units * units * denominator < target:
        units += 1
    return Fraction(units, scale)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius-json", type=Path, required=True)
    parser.add_argument("--lower-dir", type=Path, required=True)
    parser.add_argument("--goal-dir", type=Path, required=True)
    parser.add_argument("--dual-aggregate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    radius = load_json(args.radius_json)
    if radius.get("schema") != "wp19-v0.28-m15-forced-radius-v1" or radius.get("status") != "PASS_M15_FORCED_L2_RADIUS_ONLY":
        raise ValueError("M15 forced-radius result identity/status mismatch")
    radius_rows = radius.get("steps_detail", [])
    if len(radius_rows) != 240 or [r.get("step") for r in radius_rows] != list(range(240)):
        raise ValueError("M15 radius coverage mismatch")
    metadata = load_json(args.lower_dir / "metadata.json")
    if metadata.get("N") != 14 or metadata.get("steps") != 120 or metadata.get("modes") != 11513:
        raise ValueError("frozen M14 lower metadata mismatch")
    input_hashes = radius.get("frozen_inputs", {})
    for key, filename in (("lower_metadata_sha256", "metadata.json"),
                           ("lower_nodes_sha256", "nodes.npy"),
                           ("lower_rhs_sha256", "rhs.npy")):
        if input_hashes.get(key) != sha256(args.lower_dir / filename):
            raise ValueError(f"lower frozen-input hash mismatch: {key}")

    goal_paths = sorted(args.goal_dir.glob("shard_*.json"))
    if len(goal_paths) != 12:
        raise ValueError("expected 12 goal-weighted shards")
    expected_source = "8b71f5ab9b48add0a74ce4e9bb86fc904f81e925e149ca846d684a23947ca88a"
    goal_rows: dict[int, dict] = {}
    starts = []
    frozen_goal_inputs = None
    for path in goal_paths:
        shard = load_json(path)
        if shard.get("schema") != "wp19-v0.28-goal-weighted-primal-tube-shard-v1":
            raise ValueError(f"unexpected goal shard schema: {path.name}")
        if shard.get("status") != "PASS_RECONSTRUCTION_GOAL_WEIGHTED_PRIMAL_TUBE_ONLY" or shard.get("M") != 14:
            raise ValueError(f"goal shard status/M mismatch: {path.name}")
        if shard.get("count") != 20 or shard.get("start") not in range(0, 240, 20):
            raise ValueError(f"goal shard range mismatch: {path.name}")
        if shard.get("source_sha256") != expected_source:
            raise ValueError("goal-weighted source hash mismatch")
        starts.append(shard["start"])
        if frozen_goal_inputs is None:
            frozen_goal_inputs = shard.get("frozen_inputs")
        elif shard.get("frozen_inputs") != frozen_goal_inputs:
            raise ValueError("goal shard frozen-input hashes differ")
        if len(shard.get("steps", [])) != 20:
            raise ValueError(f"goal row count mismatch: {path.name}")
        for row in shard["steps"]:
            n = row.get("step")
            if not isinstance(n, int) or n in goal_rows:
                raise ValueError("duplicate or invalid goal step")
            goal_rows[n] = row
    if sorted(starts) != list(range(0, 240, 20)) or sorted(goal_rows) != list(range(240)):
        raise ValueError("goal coverage is not exactly steps 0..239")
    if frozen_goal_inputs != input_hashes:
        raise ValueError("goal shards and M15 radius bind different frozen inputs")

    dual = load_json(args.dual_aggregate)
    if (dual.get("schema") != "wp19-v0.28-reconstructed-dual-integral-fullpath-v1"
            or dual.get("status") != "PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY"
            or dual.get("step_coverage") != [0, 239]):
        raise ValueError("dual aggregate identity/status mismatch")
    if dual.get("frozen_inputs") != input_hashes:
        raise ValueError("dual aggregate and M15 radius bind different frozen inputs")
    if (radius_rows[-1].get("forced_error_L2_upper")
            != radius.get("final_forced_error_L2_upper")):
        raise ValueError("final M15 radius disagrees with the last step row")

    n14 = metadata["modes"]
    n15 = modes_in_ball(15)
    if n15 != 14147:
        raise ArithmeticError("independent M15 mode-count check failed")
    support_ratio = sqrt_upper_ratio(n15, n14)
    if support_ratio < Fraction(15, 14):
        raise ArithmeticError("support correction does not dominate the 14-to-15 cutoff factor")

    linear_total = Fraction(0)
    quadratic_total = Fraction(0)
    rows_out = []
    for n in range(240):
        row = goal_rows[n]
        # The source serialized delta with 15 places using strict outward
        # rounding. Subtracting one grid unit gives a lower bound for its
        # internal Arb upper radius, required to recover an upper for Young.
        delta_printed = dec_fraction(row["true_primal_radius_upper"])
        delta_lower = delta_printed - Fraction(1, 10**DELTA_PRINT_PLACES)
        if delta_lower <= 0:
            raise ValueError(f"delta lower bound is not positive at step {n}")
        q_old_upper = dec_fraction(row["quadratic_goal_integral_upper"])
        young_old_upper = q_old_upper / (H * delta_lower * delta_lower)
        young_m15_upper = young_old_upper * support_ratio

        e_sup = dec_fraction(radius_rows[n]["forced_error_L2_upper"])
        defect = dec_fraction(row["adjoint_ode_defect_L2_sup_upper"])
        linear = H * e_sup * defect
        quadratic = H * e_sup * e_sup * young_m15_upper
        linear_total += linear
        quadratic_total += quadratic
        rows_out.append({
            "step": n,
            "M15_error_L2_sup_upper": radius_rows[n]["forced_error_L2_upper"],
            "adjoint_defect_L2_sup_upper": row["adjoint_ode_defect_L2_sup_upper"],
            "M15_support_corrected_quadratic_upper": ceil_decimal(quadratic),
        })

    terminal_row = goal_rows[239]
    if terminal_row.get("right_endpoint_adjoint_L2_upper") is None:
        raise ValueError("terminal adjoint norm missing")
    endpoint = dec_fraction(terminal_row["right_endpoint_adjoint_L2_upper"]) * dec_fraction(radius["final_forced_error_L2_upper"])
    total = linear_total + quadratic_total + endpoint
    signed_lower = dec_fraction(dual["signed_integral_lower"])
    shard_quadratic = {
        start: sum((dec_fraction(r["M15_support_corrected_quadratic_upper"])
                    for r in rows_out if start <= r["step"] < start + 20), Fraction(0))
        for start in range(0, 240, 20)
    }
    dominant_start = max(shard_quadratic, key=shard_quadratic.get)
    top_steps = sorted(
        rows_out,
        key=lambda row: dec_fraction(row["M15_support_corrected_quadratic_upper"]),
        reverse=True,
    )[:10]

    result = {
        "schema": SCHEMA,
        "status": "NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS",
        "coverage": [0, 239],
        "mode_counts": {"M14": n14, "M15": n15},
        "M15_support_factor_upper": ceil_decimal(support_ratio, 30),
        "M15_forced_error_L2_final_upper": radius["final_forced_error_L2_upper"],
        "adjoint_defect_integral_upper": ceil_decimal(linear_total),
        "M15_support_corrected_quadratic_integral_upper": ceil_decimal(quadratic_total),
        "terminal_saved_adjoint_boundary_product_upper": ceil_decimal(endpoint),
        "sum_of_three_remainder_terms_upper": ceil_decimal(total),
        "frozen_signed_dual_integral_lower": dual["signed_integral_lower"],
        "signed_integral_minus_remainder_bound_lower": ceil_decimal(signed_lower - total),
        "dominant_quadratic_shard": {
            "start": dominant_start,
            "count": 20,
            "sum_of_per_step_upper_bounds": ceil_decimal(shard_quadratic[dominant_start]),
            "share_of_quadratic_total_approx": ceil_decimal(shard_quadratic[dominant_start] / quadratic_total, 6),
        },
        "top_quadratic_steps": [
            {"step": row["step"], "upper": row["M15_support_corrected_quadratic_upper"]}
            for row in top_steps
        ],
        "frozen_inputs": input_hashes,
        "method": (
            "Exact rational replay. Recover an upper on each original Young "
            "coefficient by dividing its outward quadratic term by a lower "
            "bound on the source delta; enlarge the cutoff and sqrt(mode-count) "
            "factors from M14 to M15; apply the exact-rational M15 forced radius to "
            "the adjoint-defect and quadratic terms; bound the terminal pairing."
        ),
        "claim_boundary": (
            "The conservative remainder upper exceeds the frozen signed-integral "
            "lower bound, so this bound set does not preserve the sign. This is "
            "a failure to close the current certificate budget, not a claim that "
            "the underlying finite-observable transfer is false. Tighter "
            "goal-oriented bounds would be needed."
        ),
        "steps_detail": rows_out,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "adjoint_defect_integral_upper": result["adjoint_defect_integral_upper"],
        "quadratic_integral_upper": result["M15_support_corrected_quadratic_integral_upper"],
        "terminal_boundary_product_upper": result["terminal_saved_adjoint_boundary_product_upper"],
        "signed_integral_lower": result["frozen_signed_dual_integral_lower"],
        "remainder_sum_upper": result["sum_of_three_remainder_terms_upper"],
        "signed_margin_lower": result["signed_integral_minus_remainder_bound_lower"],
        "dominant_quadratic_shard": result["dominant_quadratic_shard"],
    }, indent=2))


if __name__ == "__main__":
    main()

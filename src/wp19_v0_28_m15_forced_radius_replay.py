#!/usr/bin/env python3
"""Replay a conservative M15 forced L2 error radius from frozen M14 data.

The recurrence uses the exact Fourier residual of the embedded M14 cubic path
in M15 and a continuous M14 gradient bound. It uses only the Python standard
library. The input decimal strings are treated as outward upper bounds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

H = Fraction(1, 80_000)
TAYLOR_DEGREE = 20
SCHEMA = "wp19-v0.28-m15-forced-radius-v1"


def read_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    # Historical shard files have one literal backslash-n after the JSON.
    if raw.endswith("\\n"):
        raw = raw[:-2]
    return json.loads(raw)


def fraction_decimal(text: str) -> Fraction:
    return Fraction(Decimal(text))


def exp_upper(x: Fraction) -> Fraction:
    """Rational upper bound for exp(x), for 0 <= x < 1.

    Sum through degree 20, then bound the remaining positive Taylor tail by a
    geometric series whose ratio is x/22.
    """
    if x < 0 or x >= 1:
        raise ValueError("Taylor-tail bound requires 0 <= x < 1")
    total = Fraction(1)
    term = Fraction(1)
    for k in range(1, TAYLOR_DEGREE + 1):
        term = term * x / k
        total += term
    first_omitted = term * x / (TAYLOR_DEGREE + 1)
    ratio = x / (TAYLOR_DEGREE + 2)
    return total + first_omitted / (1 - ratio)


def decimal_upper(value: Fraction, places: int = 30) -> str:
    scale = 10**places
    units = (value.numerator * scale + value.denominator - 1) // value.denominator
    digits = str(units).zfill(places + 1)
    return digits[:-places] + "." + digits[-places:]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lower-dir", type=Path, required=True)
    parser.add_argument("--dual-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    metadata = read_json(args.lower_dir / "metadata.json")
    if (metadata.get("N") != 14 or metadata.get("steps") != 120
            or metadata.get("h_exact_decimal") != "0.000025"
            or metadata.get("initial_error_bound_decimal") != "0"):
        raise ValueError("lower-path frozen M14 identity mismatch")
    lower_rows = [read_json(args.lower_dir / f"{j:03d}.json") for j in range(120)]
    for j, row in enumerate(lower_rows):
        if row.get("step") != j or "gradient_Fourier_l1_upper_decimal" not in row:
            raise ValueError(f"lower segment identity mismatch at {j}")

    shard_paths = sorted(args.dual_dir.glob("dual_shard_*.json"))
    if len(shard_paths) != 12:
        raise ValueError("expected the frozen 12-shard dual integral")
    frozen_inputs = None
    rows: dict[int, dict] = {}
    for path in shard_paths:
        shard = read_json(path)
        if shard.get("schema") != "wp19-v0.28-reconstructed-dual-integral-fullpath-shard-v1":
            raise ValueError(f"unexpected shard schema: {path.name}")
        if shard.get("status") != "PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY":
            raise ValueError(f"shard status not PASS: {path.name}")
        if shard.get("count") != 20 or shard.get("start") not in range(0, 240, 20):
            raise ValueError(f"shard range mismatch: {path.name}")
        current = shard.get("frozen_inputs")
        if frozen_inputs is None:
            frozen_inputs = current
        elif current != frozen_inputs:
            raise ValueError("frozen source hashes differ across dual shards")
        if len(shard.get("steps", [])) != 20:
            raise ValueError(f"row count mismatch: {path.name}")
        for row in shard["steps"]:
            n = row.get("step")
            if not isinstance(n, int) or n in rows:
                raise ValueError("duplicate or invalid dual step")
            if row.get("interval_rational") != [f"{n}/80000", f"{n+1}/80000"]:
                raise ValueError(f"dual interval mismatch at {n}")
            if "primal_defect_L2_upper" not in row:
                raise ValueError(f"missing full M15 residual bound at {n}")
            rows[n] = row
    if sorted(rows) != list(range(240)):
        raise ValueError("dual coverage is not exactly steps 0..239")
    required_hashes = {
        "lower_metadata_sha256": sha256(args.lower_dir / "metadata.json"),
        "lower_nodes_sha256": sha256(args.lower_dir / "nodes.npy"),
        "lower_rhs_sha256": sha256(args.lower_dir / "rhs.npy"),
    }
    for key, actual in required_hashes.items():
        if frozen_inputs.get(key) != actual:
            raise ValueError(f"lower input hash mismatch: {key}")

    radius = Fraction(0)
    output_rows = []
    for n in range(240):
        segment = lower_rows[n // 2]
        gradient = fraction_decimal(segment["gradient_Fourier_l1_upper_decimal"])
        residual = fraction_decimal(rows[n]["primal_defect_L2_upper"])
        if gradient <= 0 or residual < 0:
            raise ValueError(f"nonpositive majorant at step {n}")
        exponent = gradient * H
        growth = exp_upper(exponent)
        # Variation-of-constants bound for r' <= gradient*r + residual.
        radius = growth * radius + residual * (growth - 1) / gradient
        output_rows.append({
            "step": n,
            "gradient_Fourier_l1_upper": segment["gradient_Fourier_l1_upper_decimal"],
            "M15_residual_L2_upper": rows[n]["primal_defect_L2_upper"],
            "forced_error_L2_upper": decimal_upper(radius),
        })

    result = {
        "schema": SCHEMA,
        "status": "PASS_M15_FORCED_L2_RADIUS_ONLY",
        "M_lower": 14,
        "M_error_space": 15,
        "steps": 240,
        "half_step_width": "1/80000",
        "initial_error_radius": "0",
        "final_forced_error_L2_upper": decimal_upper(radius),
        "max_forced_error_L2_upper": decimal_upper(max(
            fraction_decimal(row["forced_error_L2_upper"]) for row in output_rows
        )),
        "frozen_inputs": frozen_inputs,
        "method": (
            "L2 difference-energy inequality: transport by the embedded path and "
            "the self-transport of the error cancel; viscosity is dissipative. "
            "Use the M14 whole-segment Fourier gradient L1 bound and the M15 "
            "whole-half-segment residual L2 bound. The exponential is enclosed "
            "by an exact rational degree-20 Taylor sum plus a geometric tail."
        ),
        "claim_boundary": (
            "This bounds only the M15 solution difference from the embedded M14 "
            "reconstruction in L2, conditional on the frozen segment majorants. "
            "It does not close adjoint-weighted defect, objective endpoint, "
            "normalizer, cutoff-transfer, or continuum gates."
        ),
        "steps_detail": output_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "coverage": [0, 239],
        "final_forced_error_L2_upper": result["final_forced_error_L2_upper"],
    }, indent=2))


if __name__ == "__main__":
    main()

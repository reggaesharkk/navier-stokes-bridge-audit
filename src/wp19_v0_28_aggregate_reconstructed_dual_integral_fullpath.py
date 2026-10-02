#!/usr/bin/env python3
"""Fail-closed outward aggregation of 12 signed dual-quadrature shards."""
import argparse
import json
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path

EXPECTED_STARTS = list(range(0, 240, 20))
EXPECTED_COUNT = 20
GRID = Decimal("0.000000000000001")
SHARD_SCHEMA = "wp19-v0.28-reconstructed-dual-integral-fullpath-shard-v1"
PASS = "PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY"


def outward_sum(values, rounding):
    with localcontext() as c:
        c.prec = 120
        total = sum((Decimal(x) for x in values), Decimal(0))
        return total.quantize(GRID, rounding=rounding)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()

    files = sorted(a.shards_dir.glob("dual_shard_*.json"))
    if len(files) != len(EXPECTED_STARTS):
        raise ValueError(f"expected 12 shard files, found {len(files)}")
    shards = []
    for p in files:
        raw = p.read_text()
        # Accept the literal backslash-n marker emitted by the original shard writer.
        if raw.endswith("\\n"):
            raw = raw[:-2]
        x = json.loads(raw)
        if x.get("schema") != SHARD_SCHEMA or x.get("status") != PASS or x.get("M") != 14:
            raise ValueError(f"shard schema/status/cutoff mismatch: {p.name}")
        if x.get("count") != EXPECTED_COUNT or len(x.get("steps", [])) != EXPECTED_COUNT:
            raise ValueError(f"shard count mismatch: {p.name}")
        shards.append(x)

    shards.sort(key=lambda x: x["start"])
    starts = [x["start"] for x in shards]
    if starts != EXPECTED_STARTS:
        raise ValueError(f"missing, duplicate, or reordered ranges: {starts}")
    rows = [r for x in shards for r in x["steps"]]
    if [r["step"] for r in rows] != list(range(240)):
        raise ValueError("step coverage is not exactly 0..239 in order")
    if len({json.dumps(x["frozen_inputs"], sort_keys=True) for x in shards}) != 1:
        raise ValueError("frozen input identities differ")
    if len({x["pilot_source_sha256"] for x in shards}) != 1:
        raise ValueError("one-step pilot source identities differ")
    if len({x["shard_runner_sha256"] for x in shards}) != 1:
        raise ValueError("shard runner source identities differ")

    for n, row in enumerate(rows):
        if row["interval_rational"] != [f"{n}/80000", f"{n+1}/80000"]:
            raise ValueError(f"interval identity mismatch at step {n}")
        if Decimal(row["signed_integral_lower"]) > Decimal(row["signed_integral_upper"]):
            raise ValueError(f"invalid signed interval at step {n}")

    lower = outward_sum((r["signed_integral_lower"] for r in rows), ROUND_FLOOR)
    upper = outward_sum((r["signed_integral_upper"] for r in rows), ROUND_CEILING)
    max_adjoint = max(Decimal(r["adjoint_polynomial_L2_upper"]) for r in rows)
    max_defect = max(Decimal(r["primal_defect_L2_upper"]) for r in rows)
    out = {
        "schema": "wp19-v0.28-reconstructed-dual-integral-fullpath-v1",
        "status": PASS,
        "M": 14,
        "segments": 240,
        "step_coverage": [0, 239],
        "signed_integral_lower": str(lower),
        "signed_integral_upper": str(upper),
        "maximum_saved_adjoint_polynomial_L2_upper": str(max_adjoint),
        "maximum_reconstructed_primal_defect_L2_upper": str(max_defect),
        "pilot_source_sha256": shards[0]["pilot_source_sha256"],
        "shard_runner_sha256": shards[0]["shard_runner_sha256"],
        "frozen_inputs": shards[0]["frozen_inputs"],
        "shards": [{"start": x["start"], "count": x["count"]} for x in shards],
        "claim_boundary": "This encloses the signed dual integral for the saved cubic reconstructions over all 240 half-steps. It excludes true-path radii, terminal-gradient/Taylor and nonlinear remainders, independent normalizer transfer, and continuum conclusions.",
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\\n")
    print(json.dumps(out, indent=2), flush=True)


if __name__ == "__main__":
    main()

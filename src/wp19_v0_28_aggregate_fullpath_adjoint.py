#!/usr/bin/env python3
"""Aggregate all 240 independently replayed M14 adjoint half-segments."""
import argparse
import hashlib
import json
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path

EXPECTED_SEGMENT_SOURCE = "e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31"
EXPECTED_ADJOINT_REPORT = "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"
EXPECTED_ADJOINT_VALUES = "00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab"
EXPECTED_ADJOINT_RHS = "8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c"
EXPECTED_NODES = "e0b0a36d8b308cccb5befb3abe45777ec0775cbc7e5a76fef0011eed0fd1f7f0"
EXPECTED_RHS = "f3a55190e9cba625b7285e5ba3e09e68fa4027e7a8909d1ad80671c1ee1ef253"
H = Decimal(1) / Decimal(80000)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def verify_manifest(directory):
    directory = Path(directory)
    manifest = directory / "SHA256SUMS.txt"
    rows = manifest.read_text().splitlines()
    expected_files = {p.name for p in directory.iterdir() if p.is_file() and p.name != manifest.name}
    seen = set()
    for row in rows:
        digest, name = row.split("  ", 1)
        if name not in expected_files or name in seen or sha(directory / name) != digest:
            raise ValueError(f"manifest mismatch: {directory}/{name}")
        seen.add(name)
    if seen != expected_files:
        raise ValueError(f"manifest coverage mismatch: {directory}")

def aggregate(root):
    root = Path(root)
    segments, checks = {}, {}
    shards = sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("wp19-v0-28-M14-fullpath-shard-"))
    if len(shards) != 24:
        raise ValueError(f"expected 24 shard artifacts; found {len(shards)}")
    for shard in shards:
        verify_manifest(shard)
        for path in shard.glob("M14_segment_*.json"):
            x = json.loads(path.read_text())
            n = int(x["step"])
            if n in segments:
                raise ValueError(f"duplicate segment {n}")
            segments[n] = (path, x)
        for path in shard.glob("independent_residual_*.json"):
            x = json.loads(path.read_text())
            n = int(x["step"])
            if n in checks:
                raise ValueError(f"duplicate independent check {n}")
            checks[n] = (path, x)
    if set(segments) != set(range(240)) or set(checks) != set(range(240)):
        raise ValueError("full 0..239 segment and independent-check coverage is required")

    rows = []
    terminal_errors = set()
    incoming = None
    with localcontext() as ctx:
        ctx.prec = 90
        ctx.rounding = ROUND_CEILING
        for n in range(239, -1, -1):
            sp, s = segments[n]
            cp, c = checks[n]
            if s.get("M") != 14 or s.get("step") != n or s.get("status") != "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY":
                raise ValueError(f"segment identity/status mismatch at {n}")
            if s.get("source_sha256") != EXPECTED_SEGMENT_SOURCE or s.get("precision_bits") != 192:
                raise ValueError(f"producer identity/precision mismatch at {n}")
            if c.get("step") != n or c.get("M") != 14 or c.get("segment_sha256") != sha(sp):
                raise ValueError(f"independent report does not bind to segment {n}")
            if c.get("status") != f"INDEPENDENT_STEP_{n}_RECOMPUTATION_COMPLETE_ARCHIVE_COMPARISON_RECORDED":
                raise ValueError(f"independent recomputation missing at {n}")
            for key, expected in (
                ("adjoint_report_sha256", EXPECTED_ADJOINT_REPORT),
                ("adjoint_values_sha256", EXPECTED_ADJOINT_VALUES),
                ("adjoint_rhs_sha256", EXPECTED_ADJOINT_RHS),
                ("lower_nodes_sha256", EXPECTED_NODES),
                ("lower_rhs_sha256", EXPECTED_RHS),
            ):
                if c.get(key) != expected:
                    raise ValueError(f"frozen input identity mismatch at {n}: {key}")
            b, cb = s["bounds"], c["bounds"]
            archived_r = Decimal(b["residual_L2_upper"])
            replayed_r = Decimal(cb["independent_total_residual_L2_upper"])
            archived_l = Decimal(b["logarithmic_norm_upper"])
            replayed_l = Decimal(cb["independent_primal_strain_upper"])
            residual = max(archived_r, replayed_r)
            strain = max(archived_l, replayed_l)
            terminal_errors.add(b["terminal_adjoint_error_upper"])
            if incoming is None:
                incoming = Decimal(b["terminal_adjoint_error_upper"])
            amp = (strain * H).exp().next_plus()
            integ = ((amp - Decimal(1)) / strain) if strain else H
            outgoing = amp * incoming + integ * residual
            rows.append({
                "step": n,
                "segment_sha256": sha(sp),
                "independent_check_sha256": sha(cp),
                "incoming_adjoint_error_upper": str(incoming),
                "archived_residual_upper": str(archived_r),
                "independent_residual_upper": str(replayed_r),
                "residual_upper_used": str(residual),
                "archived_strain_upper": str(archived_l),
                "independent_strain_upper": str(replayed_l),
                "strain_upper_used": str(strain),
                "outgoing_adjoint_error_upper": str(outgoing),
            })
            incoming = outgoing
    if len(terminal_errors) != 1:
        raise ValueError("terminal error seed differs across segment records")
    rows.sort(key=lambda x: x["step"], reverse=True)
    return {
        "schema": "wp19-v0.28-M14-fullpath-adjoint-error-v1",
        "status": "PASS_FULL_M14_ADJOINT_RESIDUAL_PROPAGATION_SCALAR_CERTIFICATE",
        "M": 14,
        "adjoint_cutoff": 15,
        "segments_verified": 240,
        "step_width": "1/80000",
        "backward_order": "239 through 0",
        "terminal_error_seed": next(iter(terminal_errors)),
        "outgoing_adjoint_error_upper_step_0": str(incoming),
        "rounding": "Decimal precision 90, ROUND_CEILING, exp advanced by next_plus",
        "segments": rows,
        "claim_boundary": "Full finite M14 backward scalar adjoint-error propagation using independently recomputed whole-half-segment residual and strain bounds. This does not certify signed dual quadrature, nonlinear remainder, endpoint transfer, normalizer transfer, other cutoffs, or continuum regularity."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    result = aggregate(a.root)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k:v for k,v in result.items() if k != "segments"}, indent=2))

if __name__ == "__main__":
    main()

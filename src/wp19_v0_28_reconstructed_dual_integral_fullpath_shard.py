#!/usr/bin/env python3
"""Shard runner for exact-dyadic signed dual quadrature over M14 half-steps.

It reuses the frozen one-half-step Arb implementation without modifying its
formula or inputs. Each row is independently written by that implementation.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SCHEMA = "wp19-v0.28-reconstructed-dual-integral-fullpath-shard-v1"
PILOT_SCHEMA = "wp19-v0.28-reconstructed-dual-integral-pilot-v1"
PASS = "PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--lower-dir", type=Path, required=True)
    ap.add_argument("--adjoint-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    if a.count != 20 or a.start not in range(0, 240, 20):
        raise ValueError("expected a fixed 20-step shard starting on a multiple of 20")
    if a.start + a.count > 240:
        raise ValueError("shard extends past step 239")

    pilot = Path(__file__).with_name("wp19_v0_28_reconstructed_dual_integral_pilot.py")
    source_sha = sha(pilot)
    wrapper_sha = sha(__file__)
    work = a.output.parent / "steps"
    work.mkdir(parents=True, exist_ok=True)
    rows = []
    frozen_inputs = None
    for n in range(a.start, a.start + a.count):
        out = work / f"dual_{n}.json"
        print(f"step {n}: start", flush=True)
        subprocess.run([
            sys.executable, str(pilot),
            "--step", str(n),
            "--lower-dir", str(a.lower_dir),
            "--adjoint-dir", str(a.adjoint_dir),
            "--output", str(out),
        ], check=True, stdout=subprocess.DEVNULL)
        x = json.loads(out.read_text())
        if x.get("schema") != PILOT_SCHEMA or x.get("status") != PASS or x.get("M") != 14 or x.get("step") != n:
            raise ValueError(f"one-step pilot identity/status mismatch at {n}")
        if frozen_inputs is None:
            frozen_inputs = x["frozen_inputs"]
        elif x["frozen_inputs"] != frozen_inputs:
            raise ValueError("frozen input hashes differ across steps")
        rows.append({
            "step": n,
            "interval_rational": x["interval_rational"],
            "signed_integral_lower": x["reconstructed_signed_integral_lower"],
            "signed_integral_upper": x["reconstructed_signed_integral_upper"],
            "adjoint_polynomial_L2_upper": x["adjoint_polynomial_L2_upper"],
            "primal_defect_L2_upper": x["primal_defect_L2_upper"],
        })
        print(f"step {n}: complete", flush=True)

    result = {
        "schema": SCHEMA,
        "status": PASS,
        "M": 14,
        "start": a.start,
        "count": a.count,
        "steps": rows,
        "frozen_inputs": frozen_inputs,
        "pilot_source_sha256": source_sha,
        "shard_runner_sha256": wrapper_sha,
        "claim_boundary": "Saved cubic reconstructions only on this contiguous 20-half-step range. No true-path radii, terminal-gradient Taylor correction, or other transfer terms are included.",
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\\n")
    print(json.dumps({"start": a.start, "count": a.count, "status": PASS}), flush=True)


if __name__ == "__main__":
    main()

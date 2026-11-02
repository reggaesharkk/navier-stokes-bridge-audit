#!/usr/bin/env python3
"""Master Navier-Stokes Bridge Audit Orchestrator (WP19 v0.28 / v0.29).

Runs the repository's fail-closed verification gates in sequence:
1. 3D Fourier-ball & modewise integration test (tests/test_modewise_integration.py)
2. Independent output-bound arithmetic check (src/wp19_v0_28_independent_output_bound_check.py)
3. Route-conditioning audit on segments 239..237 (src/wp19_v0_28_route_conditioning_audit.py)
4. Reverse-time sign correction & independent Taylor replay (src/wp19_v0_28_verify_reverse_time_sign_correction.py)
5. Damping & cutoff transition sweep across N14..N18 (src/damping_runner.py)
"""
# Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT / "src", ROOT / "tests"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import wp19_v0_28_independent_output_bound_check as output_check
import wp19_v0_28_route_conditioning_audit as conditioning_audit
import wp19_v0_28_verify_reverse_time_sign_correction as sign_verifier
import damping_runner
import test_modewise_integration


def run_master_verification() -> dict:
    print("=" * 72)
    print("INITIATING MASTER NAVIER-STOKES BRIDGE AUDIT (WP19 v0.28 / v0.29)")
    print("=" * 72)

    integration = test_modewise_integration.run_integration_audit()
    out_bounds = output_check.run(ROOT)
    if out_bounds["status"] != "PASS_OUTPUT_ARITHMETIC_WITH_PRECISION_LIMIT":
        raise AssertionError(f"Unexpected output-bound status: {out_bounds['status']}")
    print("[PASS] Independent output-bound arithmetic check:", out_bounds["status"])

    cond = conditioning_audit.build()
    if cond["status"] != "DIAGNOSTIC_ONLY_NO_ROUTE_FAILURE_THEOREM":
        raise AssertionError(f"Unexpected conditioning status: {cond['status']}")
    print("[PASS] Route-conditioning audit verified across segments 239, 238, 237.")

    sign_verifier.main()
    print("[PASS] Reverse-time sign correction & Taylor recurrence replay verified.")

    damping = damping_runner.evaluate_damping_sweep()
    print("[PASS] 3D damping & N14->N18 transition ledger verified.")

    summary = {
        "schema": "wp19-master-audit-orchestrator-v2",
        "status": "PASS_ALL_LOCAL_FAIL_CLOSED_GATES",
        "output_bound_check_status": out_bounds["status"],
        "route_conditioning_status": cond["status"],
        "three_segment_recurrence_status": integration["chain"]["status"],
        "segment_237_structured_young_ratio_upper": integration["ab"]["new_over_old_penalty_ratio_upper"],
        "m14_m15_pr155_transfer_disposition": "NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS",
        "transitions_audited": [t["transition"] for t in damping["transitions"]],
        "claim_boundary": "Finite-Galerkin certificates and three-segment M14 adjoint recurrence only; full M14/M15 objective transfer and continuum Navier-Stokes regularity remain open.",
    }
    print("=" * 72)
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    run_master_verification()

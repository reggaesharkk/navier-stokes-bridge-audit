#!/usr/bin/env python3
"""Integration Test for 3D Modewise Dissipation Control & WP19 v0.28 Segment Bounds.

Validates:
1. Exact 3D solenoidal projection and divergence-free constraint on the frozen
   112-pair rational witness in DealiasedSystem.
2. Exact 3D Fourier ball enumeration for N=11, N=14, and N=15.
3. Modewise low/high spectral projection (P11 vs high shells).
4. Outward Decimal interval verification of the 3 frozen M14 Arb segments
   (239, 238, 237) and the structured Fourier-Young 2x tightening gate on step 237.
"""
# Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
from __future__ import annotations

import os
import sys
from decimal import Decimal
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from modewise_remainder_control import (
    build_witness_galerkin_state,
    compute_modewise_projection,
    compute_solenoidal_divergence_defect,
    enumerate_fourier_ball,
    estimate_modewise_remainder_bound,
    evaluate_frozen_segment_237_structured_bound,
)
from interval_modewise_verifier import (
    compute_certified_remainder_interval,
    verify_frozen_m14_segment_chain,
)


def run_integration_audit() -> dict:
    print("Initializing 3D Navier-Stokes Modewise & Segment Integration Audit...")

    # 1. Verify exact 3D Fourier ball enumerations used in WP19 v0.14 and v0.28
    b11 = enumerate_fourier_ball(11)
    b14 = enumerate_fourier_ball(14)
    b15 = enumerate_fourier_ball(15)
    assert (b11["nonzero_mode_count"], b11["sum_k_squared"]) == (5574, 404724), b11
    assert (b14["mode_count_including_zero"], b14["sum_k_squared"]) == (11513, 1355442), b14
    assert (b15["mode_count_including_zero"], b15["max_k_squared"]) == (14147, 225), b15
    print("-> [PASS] 3D Fourier ball enumerations (N=11, 14, 15) match WP19 invariants.")

    # 2. Load frozen 112-pair rational witness into 3D DealiasedSystem(14)
    sys14, state14 = build_witness_galerkin_state(14)
    max_div = compute_solenoidal_divergence_defect(sys14, state14)
    print(f"-> [PASS] 3D solenoidal divergence check on 112-pair witness: max |k.u_k| = {max_div:.2e}")
    assert max_div < 1e-12, f"Divergence defect too large: {max_div}"

    # 3. Modewise 3D projection onto P11 vs shells 12..14
    u_low, u_high = compute_modewise_projection(state14, cutoff_M=11, system=sys14)
    u_high_norm = float(np.linalg.norm(u_high))
    total_sq = float(np.linalg.norm(state14) ** 2)
    orth_err = abs(total_sq - (float(np.linalg.norm(u_low) ** 2) + u_high_norm ** 2)) / max(1.0, total_sq)
    assert orth_err < 1e-12, f"Parseval orthogonality defect: {orth_err}"
    bound = estimate_modewise_remainder_bound(u_high_norm, viscosity=0.1, cutoff_M=11)
    interval = compute_certified_remainder_interval(u_high_norm, viscosity=0.1, cutoff_M=11)
    assert Decimal(interval["upper_bound_decimal"]) >= bound
    assert interval["is_certified"] is True
    print(f"-> [PASS] 3D modewise projection & interval enclosure: [{interval['lower_bound_decimal']}, {interval['upper_bound_decimal']}]")

    # 4. Verify frozen M14 segments (239, 238, 237) and structured Young A/B tightening
    chain = verify_frozen_m14_segment_chain()
    assert chain["status"] == "PASS_THREE_SEGMENT_BACKWARD_RECURRENCE_VERIFIED"
    assert len(chain["rows"]) == 3
    ab = evaluate_frozen_segment_237_structured_bound()
    assert ab["passes_2x_tightening_gate"] is True
    assert ab["new_over_old_penalty_ratio_upper"] == "0.334854921854"
    print(f"-> [PASS] Frozen M14 segments (239..237) & step-237 structured Young ratio ({ab['new_over_old_penalty_ratio_upper']}) verified.")
    print("Integration audit completed successfully. All checks passed.")
    return {"chain": chain, "ab": ab}


if __name__ == "__main__":
    run_integration_audit()

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
from flint import acb, arb
from wp19_v0_28_goal_weighted_targeted_m15_support import quadratic_schur_coefficient
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



def test_m15_quadratic_schur_coefficient_uses_weighted_fourier_l1():
    system = DealiasedSystem(1, nu=0.1)
    control = []
    for raw_mode in system.modes:
        mode = tuple(int(v) for v in raw_mode)
        if mode in ((1, 0, 0), (-1, 0, 0)):
            control.append([acb(0), acb(2), acb(0)])
        elif mode == (0, 0, 0):
            control.append([acb(100), acb(0), acb(0)])
        else:
            control.append([acb(0), acb(0), acb(0)])
    upper = quadratic_schur_coefficient(system, control)
    assert upper.overlaps(arb(4)), upper


def test_finite_mode_quadratic_schur_inequality_exactly():
    # Exact finite control: lambda is supported on the six unit axial modes,
    # each with coefficient norm one. Thus its weighted Fourier L1 sum is 6.
    from fractions import Fraction

    errors = [
        (x, y, z)
        for x in range(-1, 2)
        for y in range(-1, 2)
        for z in range(-1, 2)
        if x*x + y*y + z*z <= 1
    ]
    adjoint = {
        mode: Fraction(1)
        for mode in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    }
    weighted_l1 = sum(adjoint.values())
    row_sums = []
    matrix = []
    for p in errors:
        row = []
        for q in errors:
            k = tuple(-p[d] - q[d] for d in range(3))
            row.append(adjoint.get(k, Fraction(0)))
        row_sums.append(sum(row))
        matrix.append(row)
    assert max(row_sums) <= weighted_l1

    amplitudes = [Fraction(i + 1, len(errors) + 1) for i in range(len(errors))]
    quadratic = sum(
        matrix[i][j] * amplitudes[i] * amplitudes[j]
        for i in range(len(errors))
        for j in range(len(errors))
    )
    norm_squared = sum(value * value for value in amplitudes)
    assert quadratic <= weighted_l1 * norm_squared

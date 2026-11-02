#!/usr/bin/env python3
"""Automated High-Frequency Damping & Cutoff Escalation Evaluator (WP19 N14-N18).

Replaces the synthetic 2D sweep with exact 3D Fourier-Galerkin ball metrics,
v0.19 boundary-annulus direct-shell bounds, and v0.21/v0.27b certified
terminal radii across transitions 14->15, 15->16, 16->17, and 17->18.
"""
# Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
from __future__ import annotations

import json
import sys
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from modewise_remainder_control import enumerate_fourier_ball

# Certified values from notes/WP19_CURRENT_STATUS_2026_09_30.md and
# notes/WP19_v0_27b_EXECUTED_RESULT_2026_09_30.md
CERTIFIED_CHAIN_N14_N18 = {
    14: {
        "F_endpoint_interval": ["-89.015834781", "-85.160766265"],
        "terminal_L2_error_upper": "0.000012825905",
        "normalizer_lower": "48850.68586052",
        "v027b_gradient_variation_L2_upper": "15845467881.27747",
        "v027b_taylor_over_margin_upper": "0.000001497069",
    },
    15: {
        "F_endpoint_interval": ["-88.958192681", "-84.896722370"],
        "terminal_L2_error_upper": "0.000013195722",
        "normalizer_lower": "48856.49133823",
        "v027b_gradient_variation_L2_upper": "16301397742.549378",
        "v027b_taylor_over_margin_upper": "0.000001655541",
    },
    16: {
        "F_endpoint_interval": ["-88.828357601", "-84.589032046"],
        "terminal_L2_error_upper": "0.000013456103",
        "normalizer_lower": "48858.17452511",
        "v027b_gradient_variation_L2_upper": "16622536128.074724",
        "v027b_taylor_over_margin_upper": "0.000001735717",
    },
    17: {
        "F_endpoint_interval": ["-88.682140170", "-84.277596371"],
        "terminal_L2_error_upper": "0.000013665541",
        "normalizer_lower": "48860.35300815",
        "v027b_gradient_variation_L2_upper": "16881279926.025994",
        "v027b_taylor_over_margin_upper": "0.000001794275",
    },
    18: {
        "F_endpoint_interval": ["-88.699660529", "-84.159654865"],
        "terminal_L2_error_upper": "0.000013774643",
        "normalizer_lower": "48860.59568947",
    },
}


def evaluate_damping_sweep() -> dict:
    """Evaluate 3D shell damping rates and v0.19 boundary-annulus scaling for M=14..17."""
    nu = Decimal("0.1")
    h_half = Decimal(1) / Decimal(80000)
    ball_11 = enumerate_fourier_ball(11)
    if ball_11["nonzero_mode_count"] != 5574 or ball_11["sum_k_squared"] != 404724:
        raise AssertionError(f"P11 Fourier enumeration mismatch: {ball_11}")

    transitions = []
    with localcontext() as ctx:
        ctx.prec = 50
        ctx.rounding = ROUND_CEILING
        c11 = Decimal(ball_11["sum_k_squared"]).sqrt().next_plus()
        for M in (14, 15, 16, 17):
            low_ball = enumerate_fourier_ball(M)
            high_ball = enumerate_fourier_ball(M + 1)
            new_shell_modes = high_ball["mode_count_including_zero"] - low_ball["mode_count_including_zero"]
            min_shell_ksq = M * M + 1
            max_shell_ksq = (M + 1) * (M + 1)
            min_dissip = nu * Decimal(min_shell_ksq)
            max_dissip = nu * Decimal(max_shell_ksq)
            annulus_factor = (Decimal(1) / Decimal(M * (M - 11))) + (Decimal(1) / Decimal(M * M))
            cert = CERTIFIED_CHAIN_N14_N18[M]
            transitions.append({
                "transition": f"{M}->{M+1}",
                "low_cutoff_M": M,
                "high_cutoff_M": M + 1,
                "low_mode_count": low_ball["mode_count_including_zero"],
                "high_mode_count": high_ball["mode_count_including_zero"],
                "new_shell_mode_count": new_shell_modes,
                "new_shell_ksq_range": [min_shell_ksq, max_shell_ksq],
                "viscous_damping_rate_range_per_unit_time": [str(min_dissip), str(max_dissip)],
                "half_step_damping_exponent_range": [
                    str(min_dissip * h_half),
                    str(max_dissip * h_half),
                ],
                "v019_boundary_annulus_factor_1_over_M_M11_plus_1_over_M2": str(annulus_factor),
                "certified_lower_terminal_L2_error_upper": cert["terminal_L2_error_upper"],
                "v027b_gradient_variation_L2_upper": cert["v027b_gradient_variation_L2_upper"],
                "v027b_taylor_over_margin_upper": cert["v027b_taylor_over_margin_upper"],
            })

    return {
        "schema": "wp19-damping-and-cutoff-transition-audit-v2",
        "P11_fixed_support": {
            "nonzero_modes": ball_11["nonzero_mode_count"],
            "sum_k_squared": ball_11["sum_k_squared"],
            "C11_upper": str(c11),
        },
        "transitions": transitions,
        "claim_boundary": "Exact 3D Fourier-ball damping and certified N14-N18 endpoint ledger only; no all-N or continuum theorem.",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate_damping_sweep(), indent=2))

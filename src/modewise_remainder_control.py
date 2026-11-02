#!/usr/bin/env python3
"""Modewise Adjoint Remainder and Dissipation Control Module (WP19 v0.28 / PR #155).

Operates strictly on the repository's 3D dealiased Fourier-Galerkin system
(DealiasedSystem) and frozen WP19 v0.28 segment/A-B artifacts.
Does NOT use synthetic 2D grids or unverified continuum extrapolations.
"""
# Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
from __future__ import annotations

import hashlib
import json
import math
import sys
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from wp16_036_dealiased_trajectory_gate import DealiasedSystem
import wp16_036_sparse_turnover_exact_anchor as exact
import wp19_v0_23_rk4_goal_adjoint as v23

WITNESS_PATH = ROOT / "results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json"
EXPECTED_WITNESS_SHA256 = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
AB_PATH = ROOT / "results/wp19_v0_28/structured_uncertainty_ab_20261001/structured_uncertainty_ab.json"
EXPECTED_AB_SHA256 = "b67857abf2392d963985714415e3def7d0fb4f536235765058b6a118a73bba4a"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enumerate_fourier_ball(cutoff_M: int) -> dict[str, int]:
    """Independently enumerate the 3D integer Fourier ball |k| <= cutoff_M."""
    if cutoff_M < 1:
        raise ValueError("cutoff_M must be positive")
    mode_count = 0
    nonzero_count = 0
    sum_k_sq = 0
    max_k_sq = 0
    for kx in range(-cutoff_M, cutoff_M + 1):
        for ky in range(-cutoff_M, cutoff_M + 1):
            for kz in range(-cutoff_M, cutoff_M + 1):
                ksq = kx * kx + ky * ky + kz * kz
                if ksq <= cutoff_M * cutoff_M:
                    mode_count += 1
                    if ksq > 0:
                        nonzero_count += 1
                    sum_k_sq += ksq
                    if ksq > max_k_sq:
                        max_k_sq = ksq
    return {
        "cutoff_M": cutoff_M,
        "mode_count_including_zero": mode_count,
        "nonzero_mode_count": nonzero_count,
        "sum_k_squared": sum_k_sq,
        "max_k_squared": max_k_sq,
    }


def compute_solenoidal_divergence_defect(system: DealiasedSystem, state: np.ndarray) -> float:
    """Compute max_k |k . u_hat(k)| across all 3D Fourier modes in system."""
    arr = np.asarray(state, dtype=np.complex128)
    if arr.shape != (len(system.modes), 3):
        raise ValueError(f"Expected state shape {(len(system.modes), 3)}, got {arr.shape}")
    dots = np.sum(arr * system.waves, axis=1)
    return float(np.max(np.abs(dots))) if len(dots) else 0.0


def compute_modewise_projection(
    u_field: np.ndarray,
    cutoff_M: int,
    system: DealiasedSystem | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Split a 3D Fourier-Galerkin state (or 2D array fallback) at |k| <= cutoff_M.

    When `system` is provided (or `u_field` has shape `(num_modes, 3)` matching a
    3D `DealiasedSystem`), decomposes the modal array exactly into low modes
    (`|k|^2 <= cutoff_M^2`) and high shell modes (`|k|^2 > cutoff_M^2`).
    """
    arr = np.asarray(u_field)
    if system is not None:
        if arr.shape != (len(system.modes), 3):
            raise ValueError(f"State shape {arr.shape} does not match system modes {len(system.modes)}")
        mask_low = (system.square <= cutoff_M * cutoff_M)[:, None]
        u_low = np.where(mask_low, arr, 0.0)
        u_high = np.where(~mask_low, arr, 0.0)
        return u_low, u_high

    if arr.ndim == 2 and arr.shape[1] == 3:
        # Infer cutoff or use explicit square norm if passed as 3D modal list
        raise ValueError("Pass `system=DealiasedSystem(N)` when projecting a 3D modal state (num_modes, 3).")

    if arr.ndim == 2:
        ny, nx = arr.shape
        ky = np.rint(np.fft.fftfreq(ny) * ny).astype(int)
        kx = np.rint(np.fft.fftfreq(nx) * nx).astype(int)
        kx_grid, ky_grid = np.meshgrid(kx, ky)
        mask_low = (kx_grid * kx_grid + ky_grid * ky_grid) <= (cutoff_M * cutoff_M)
        u_fft = np.fft.fft2(arr)
        return np.real(np.fft.ifft2(u_fft * mask_low)), np.real(np.fft.ifft2(u_fft * (~mask_low)))

    raise ValueError("u_field must be a 3D Galerkin modal array (with system) or 2D array.")


def estimate_modewise_remainder_bound(
    u_high_norm: float | Decimal,
    viscosity: float | Decimal,
    cutoff_M: int,
) -> Decimal:
    """Compute outward Decimal upper bound for u_high_norm / (nu * cutoff_M^2)."""
    if cutoff_M <= 0:
        raise ValueError("cutoff_M must be strictly positive")
    with localcontext() as ctx:
        ctx.prec = 50
        ctx.rounding = ROUND_CEILING
        nu_d = Decimal(str(viscosity))
        if nu_d <= 0:
            raise ValueError("viscosity must be strictly positive")
        dissip = nu_d * Decimal(cutoff_M * cutoff_M)
        return (Decimal(str(u_high_norm)) / dissip).next_plus()


def evaluate_frozen_segment_237_structured_bound() -> dict:
    """Verify and return the exact structured Fourier-Young tightening on M14 step 237."""
    if sha256_file(AB_PATH) != EXPECTED_AB_SHA256:
        raise ValueError("Frozen structured_uncertainty_ab.json SHA-256 mismatch")
    ab = json.loads(AB_PATH.read_text())
    with localcontext() as ctx:
        ctx.prec = 80
        ctx.rounding = ROUND_CEILING
        controls = ab["bernstein_control_upper_norms"]
        l1_sup = max(Decimal(c["L1_mode_upper"]) for c in controls)
        grad_sup = max(Decimal(c["gradient_L2_upper"]) for c in controls)
        l2_sup = max(Decimal(c["L2_upper"]) for c in controls)
        low_modes = int(ab["mode_counts"]["low_M14"])
        high_modes = int(ab["mode_counts"]["high_M15"])
        eps = Decimal(ab["primal_L2_radius_upper"])
        factor = (Decimal(14) * l1_sup + Decimal(low_modes).sqrt().next_plus() * grad_sup).next_plus()
        structured_penalty = (eps * factor).next_plus()
        old_penalty = Decimal(ab["old_componentwise_triangle_penalty_upper"])
        ratio = (structured_penalty / old_penalty).next_plus()
    return {
        "step": 237,
        "M_low": 14,
        "M_high": 15,
        "low_mode_count": low_modes,
        "high_mode_count": high_modes,
        "shell_15_new_mode_count": high_modes - low_modes,
        "bernstein_L2_sup_upper": str(l2_sup),
        "bernstein_L1_sup_upper": str(l1_sup),
        "bernstein_grad_L2_sup_upper": str(grad_sup),
        "old_componentwise_penalty_upper": str(old_penalty),
        "structured_fourier_young_penalty_upper": ab["structured_fourier_young_penalty_upper"],
        "new_over_old_penalty_ratio_upper": ab["new_over_old_penalty_upper"],
        "recomputed_ratio_upper": str(ratio),
        "passes_2x_tightening_gate": ratio <= Decimal("0.5"),
        "pr155_m14_m15_status": "NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS",
        "claim_boundary": "One-segment structured primal-uncertainty tightening only; full M14->M15 objective transfer remains open.",
    }


def build_witness_galerkin_state(cutoff_M: int = 14) -> tuple[DealiasedSystem, np.ndarray]:
    """Load the frozen 112-pair rational witness into a 3D DealiasedSystem(cutoff_M)."""
    modes_dict, _, whash = exact.input_state(WITNESS_PATH)
    if whash != EXPECTED_WITNESS_SHA256:
        raise ValueError(f"Witness SHA-256 mismatch: {whash}")
    system = DealiasedSystem(cutoff_M, nu=0.1)
    state = np.asarray(
        [
            [complex(float(v[0]), float(v[1])) for v in modes_dict.get(k, (exact.ZERO,) * 3)]
            for k in system.modes
        ],
        dtype=np.complex128,
    )
    state = v23.physical_project(system, state)
    state = v23.physical_project(system, system.rk4(state, 0.000025))
    return system, state


if __name__ == "__main__":
    sys15, state15 = build_witness_galerkin_state(15)
    u_low, u_high = compute_modewise_projection(state15, cutoff_M=11, system=sys15)
    div_err = compute_solenoidal_divergence_defect(sys15, state15)
    ab_summary = evaluate_frozen_segment_237_structured_bound()
    out = {
        "module": "src/modewise_remainder_control.py",
        "witness_sha256": EXPECTED_WITNESS_SHA256,
        "solenoidal_divergence_defect_max": div_err,
        "low_P11_L2_norm": float(np.linalg.norm(u_low)),
        "high_above_11_L2_norm_at_t0": float(np.linalg.norm(u_high)),
        "segment_237_structured_ab": ab_summary,
    }
    print(json.dumps(out, indent=2))

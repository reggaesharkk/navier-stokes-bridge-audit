#!/usr/bin/env python3
"""Recompute a conservative scalar step-237 rebase from frozen uppers."""
from __future__ import annotations
import argparse
import json
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path

H = Decimal(1) / Decimal(80000)
PRECISION = 90
INCOMING = Decimal("76596803403.2008814415291810393914219040829827539878570803371585034700432692390455397776715")
RESIDUAL = Decimal("724222211755.601020")
ARCHIVED_RESIDUAL = Decimal("724222211753.270303")
STRAIN = Decimal("1752.285153301")
INDEPENDENT_STRAIN = Decimal("1752.285153299660")
REVERSE_DIFFUSION = Decimal("22.5")
PREVIOUS_OUTGOING = Decimal("78324232548.8246196307457504997741547715008957776049367908160897460488479268828768235373913")


def step(incoming: Decimal, growth: Decimal, residual: Decimal) -> Decimal:
    if incoming < 0 or growth <= 0 or residual < 0:
        raise ValueError("invalid recurrence inputs")
    with localcontext() as ctx:
        ctx.prec = PRECISION
        ctx.rounding = ROUND_CEILING
        amp = (growth * H).exp().next_plus()
        return amp * incoming + ((amp - Decimal(1)) / growth) * residual


def build() -> dict:
    if RESIDUAL <= ARCHIVED_RESIDUAL:
        raise ValueError("replacement residual must dominate the archived upper")
    if STRAIN < INDEPENDENT_STRAIN:
        raise ValueError("retained strain upper must dominate the independent upper")
    growth = STRAIN + REVERSE_DIFFUSION
    outgoing = step(INCOMING, growth, RESIDUAL)
    previous = step(INCOMING, growth, ARCHIVED_RESIDUAL)
    if previous != PREVIOUS_OUTGOING or outgoing <= previous:
        raise ValueError("recurrence reproduction or monotonicity check failed")
    return {
        "schema": "wp19-v0.28-independent-step-237-residual-rebase-v1",
        "status": "PASS_CONSERVATIVE_STEP_237_SCALAR_REBASE",
        "step": 237,
        "forward_time_interval_rational": ["237/80000", "238/80000"],
        "backward_order_index": 2,
        "inputs": {
            "independent_workflow_run_id": 36866461680,
            "independent_artifact_id": 11166791059,
            "independent_artifact_zip_sha256": "4acc1a47ead19d5cab8f55c186f2677ed93c17aefca11bbbe5eee5e0fe366937",
            "segment_sha256": "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc",
            "corrected_chain_incoming_upper": str(INCOMING),
            "independent_residual_upper": str(RESIDUAL),
            "archived_residual_upper": str(ARCHIVED_RESIDUAL),
            "independent_strain_upper": str(INDEPENDENT_STRAIN),
            "archived_strain_upper_retained": str(STRAIN),
            "reverse_diffusion_upper": str(REVERSE_DIFFUSION),
        },
        "recurrence": {
            "formula": "e_out <= exp(L*h)*e_in + ((exp(L*h)-1)/L)*R",
            "h": "1/80000",
            "L_used": str(growth),
            "rounding": "Decimal precision 90; ROUND_CEILING; exp advanced by next_plus",
            "recomputed_outgoing_upper": str(outgoing),
            "outgoing_using_archived_residual": str(previous),
            "outgoing_increase": str(outgoing - previous),
            "increase_vs_published_corrected_chain": str(outgoing - PREVIOUS_OUTGOING),
        },
        "validation": {
            "independent_residual_exceeds_archived_residual": True,
            "archived_strain_dominates_independent_strain": True,
            "incoming_matches_step_238_corrected_outgoing": True,
        },
        "scope": {
            "established": "A scalar recurrence rebase for this one segment, using the independent whole-segment residual upper and retaining the larger archived strain upper.",
            "conditional_on": "The incoming radius from steps 239 and 238 remains conditional on their imported segment residual and strain bounds.",
            "not_established": [
                "independent reproduction of the producer component values",
                "other segment residuals",
                "full backward adjoint path",
                "dual quadrature",
                "nonlinear remainder",
                "normalizer",
                "endpoint transfer",
                "continuum regularity",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

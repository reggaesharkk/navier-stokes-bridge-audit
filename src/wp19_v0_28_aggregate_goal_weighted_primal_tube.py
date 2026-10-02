#!/usr/bin/env python3
"""Fail-closed outward-decimal aggregation for 12 goal-weighted path shards."""
import argparse, json
from decimal import Decimal, localcontext, ROUND_CEILING
from pathlib import Path

EXPECTED_STARTS=list(range(0,240,20))
EXPECTED_COUNT=20
GRID=Decimal("0.000000000001")

def outward_sum(values):
    with localcontext() as c:
        c.prec=100
        c.rounding=ROUND_CEILING
        total=sum((Decimal(x) for x in values),Decimal(0))
        return total.quantize(GRID,rounding=ROUND_CEILING)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--shards-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    files=sorted(a.shards_dir.glob("shard_*.json"))
    if len(files)!=len(EXPECTED_STARTS):
        raise ValueError(f"expected {len(EXPECTED_STARTS)} shard artifacts, found {len(files)}")
    shards=[]
    for p in files:
        x=json.loads(p.read_text())
        if x.get("schema")!="wp19-v0.28-goal-weighted-primal-tube-shard-v1" or x.get("status")!="PASS_RECONSTRUCTION_GOAL_WEIGHTED_PRIMAL_TUBE_ONLY" or x.get("M")!=14:
            raise ValueError(f"shard schema/status/cutoff mismatch: {p.name}")
        if x.get("count")!=EXPECTED_COUNT or len(x.get("steps",[]))!=EXPECTED_COUNT:
            raise ValueError(f"shard count mismatch: {p.name}")
        shards.append(x)
    shards.sort(key=lambda x:x["start"])
    starts=[x["start"] for x in shards]
    if starts!=EXPECTED_STARTS:
        raise ValueError(f"missing, duplicate, or reordered ranges: {starts}")
    all_rows=[r for x in shards for r in x["steps"]]
    numbers=[r["step"] for r in all_rows]
    if numbers!=list(range(240)):
        raise ValueError("step coverage is not exactly 0..239 in order")
    frozen={json.dumps(x["frozen_inputs"],sort_keys=True) for x in shards}
    sources={x.get("source_sha256") for x in shards}
    if len(frozen)!=1 or len(sources)!=1:
        raise ValueError("shard source or frozen input identities differ")
    if any(r.get("terminal_endpoint_product_upper") is not None for r in all_rows[:-1]):
        raise ValueError("unexpected terminal endpoint field before final interval")
    terminal=all_rows[-1].get("terminal_endpoint_product_upper")
    if terminal is None:
        raise ValueError("final endpoint bound missing")
    linear=outward_sum(r["linear_goal_integral_upper"] for r in all_rows)
    quadratic=outward_sum(r["quadratic_goal_integral_upper"] for r in all_rows)
    combined=outward_sum([linear,quadratic])
    out={
      "schema":"wp19-v0.28-goal-weighted-primal-tube-fullpath-v1",
      "status":"PASS_RECONSTRUCTION_GOAL_WEIGHTED_PRIMAL_TUBE_ONLY",
      "M":14,"segments":240,"step_coverage":[0,239],
      "linear_goal_integral_upper_sum":linear,
      "quadratic_goal_remainder_upper_sum":quadratic,
      "combined_interior_primal_tube_upper":combined,
      "initial_boundary_term_upper":"0 (shared exact initial datum)",
      "terminal_reconstruction_boundary_product_upper":terminal,
      "internal_boundary_rule":"Internal terms cancel by telescoping only for one continuous primal error path and the shared saved adjoint values at common nodes.",
      "source_sha256":next(iter(sources)),
      "frozen_inputs":json.loads(next(iter(frozen))),
      "shards":[{"start":x["start"],"count":x["count"]} for x in shards],
      "claim_boundary":"This aggregates only the reconstruction-based primal-tube contribution and the saved-adjoint center endpoint product. It excludes terminal-gradient uncertainty/Taylor remainder, adjoint certificate transfers outside this integration-by-parts identity, the independent normalizer, and continuum conclusions."
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2),flush=True)

if __name__=="__main__": main()

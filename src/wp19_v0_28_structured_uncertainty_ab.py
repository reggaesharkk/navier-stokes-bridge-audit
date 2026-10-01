#!/usr/bin/env python3
"""Frozen one-segment A/B audit of the v0.28 primal-uncertainty residual bound.

This does not recompute the adjoint residual. It compares the archived
componentwise/triangle uncertainty penalty with a structured Fourier L2
Young bound for the same M14 segment 237, frozen primal radius, and Hermite
adjoint polynomial. All input binary64 values are imported as exact dyadics;
Arb encloses every norm and arithmetic operation.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
from flint import acb, arb, ctx
import wp19_v0_28_adjoint_segment_arb as base
from wp16_036_dealiased_trajectory_gate import DealiasedSystem

ctx.prec = 192
M, STEP = 14, 237
SEGMENT_SHA = "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc"
REPORT_SHA = "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"
VALUES_SHA = "00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab"
RHS_SHA = "8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c"
FROZEN = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}
PREDECLARED_MAX_RATIO = arb("0.5")  # require at least a 2x reduction to call it material

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--adjoint-dir",type=Path,required=True)
    ap.add_argument("--segment",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    seg=json.loads(a.segment.read_text())
    if sha(a.segment)!=SEGMENT_SHA: raise ValueError("segment 237 baseline hash mismatch")
    if seg.get("schema")!="wp19-v0.28-adjoint-segment-arb-v2" or seg.get("step")!=STEP or seg.get("M")!=M or seg.get("frozen")!=FROZEN:
        raise ValueError("baseline segment identity mismatch")
    if seg.get("status")!="CONTINUOUS_SEGMENT_ENCLOSURE_ONLY": raise ValueError("baseline segment status mismatch")
    report=a.adjoint_dir/"M14_arb_vjp_point.json"
    if sha(report)!=REPORT_SHA: raise ValueError("frozen M14 adjoint report hash mismatch")
    rec=json.loads(report.read_text()).get("adjoint_reconstruction",{})
    values=a.adjoint_dir/rec.get("values_file","")
    rhs=a.adjoint_dir/rec.get("rhs_file","")
    if sha(values)!=VALUES_SHA or sha(rhs)!=RHS_SHA: raise ValueError("frozen M14 adjoint arrays hash mismatch")
    if rec.get("values_sha256")!=VALUES_SHA or rec.get("rhs_sha256")!=RHS_SHA: raise ValueError("report does not bind frozen adjoint arrays")

    high=DealiasedSystem(M+1,nu=.1)
    low=DealiasedSystem(M,nu=.1)
    adj=np.load(values,mmap_mode="r"); arhs=np.load(rhs,mmap_mode="r")
    if adj.shape!=(241,len(high.modes),3) or arhs.shape!=adj.shape: raise ValueError("adjoint path array shape mismatch")
    # Same exact-dyadic projection, Hermite interpolant and Bernstein controls as v0.28.
    rows=[base.projected_rows(high,x) for x in (adj[STEP],adj[STEP+1],arhs[STEP],arhs[STEP+1])]
    L=base.hermite(*rows,base.HALF_H)
    controls=base.bernstein(L)
    per=[]
    for b in controls:
        l1=arb(0); grad2=arb(0); l2=base.norm(b)
        for k,ksq,row in zip(high.modes,high.square,b):
            v=base.norm([row])
            l1+=v
            grad2+=arb(int(ksq))*(v**2)
        per.append({"L2_upper":l2.upper(),"L1_mode_upper":l1.upper(),"gradient_L2_upper":grad2.sqrt().upper()})
    l2sup=max(x["L2_upper"] for x in per)
    l1sup=max(x["L1_mode_upper"] for x in per)
    grad_sup=max(x["gradient_L2_upper"] for x in per)
    eps=arb(seg["bounds"]["true_primal_radius_upper"])
    old_penalty=arb(seg["bounds"]["primal_uncertainty_residual_penalty_upper"])
    old_factor=(arb(sum(int(x) for x in low.square)).sqrt()+(M+1)*arb(len(low.modes)).sqrt())*l2sup
    # Bilinear VJP perturbation, after the norm-one Leray projection:
    # ||(grad e)^T L||_2 <= || |k|e ||_2 ||L||_1 <= M||e||_2||L||_1;
    # ||(e.grad)L||_2 <= ||e||_1 ||grad L||_2 <= sqrt(n)||e||_2||grad L||_2.
    new_factor=(M*l1sup+arb(len(low.modes)).sqrt()*grad_sup).upper()
    new_penalty=(eps*new_factor).upper()
    ratio=(new_penalty/old_penalty).upper()
    status="MATERIAL_TIGHTENING" if ratio<=PREDECLARED_MAX_RATIO else "NO_MATERIAL_TIGHTENING"
    out={
      "schema":"wp19-v0.28-structured-primal-uncertainty-ab-v1",
      "status":status,"M":M,"step":STEP,"interval_rational":["237/80000","238/80000"],
      "precision_bits":ctx.prec,"baseline_segment_sha256":sha(a.segment),
      "adjoint_report_sha256":sha(report),"adjoint_values_sha256":sha(values),"adjoint_rhs_sha256":sha(rhs),
      "frozen":FROZEN,"predeclared_materiality_threshold_new_over_old":"0.5",
      "primal_L2_radius_upper":base.safe_decimal_upper(eps,15),
      "old_componentwise_triangle_penalty_upper":base.safe_decimal_upper(old_penalty,6),
      "old_formula_recomputed_factor_upper":base.safe_decimal_upper(old_factor,12),
      "structured_fourier_young_factor_upper":base.safe_decimal_upper(new_factor,12),
      "structured_fourier_young_penalty_upper":base.safe_decimal_upper(new_penalty,6),
      "new_over_old_penalty_upper":base.safe_decimal_upper(ratio,12),
      "bernstein_control_upper_norms":[{k:base.safe_decimal_upper(v,12) for k,v in x.items()} for x in per],
      "mode_counts":{"low_M14":len(low.modes),"high_M15":len(high.modes)},
      "method":"For each time Bernstein control, compute Arb bounds on sum_k |L_k|, |||k|L_k||_2, and ||L||_2. Apply discrete Young inequalities to the bilinear VJP perturbation and the norm-one Leray projection. The global primal error enters only through its frozen L2 radius; divergence-free/reality fields are included as a subset of the ambient L2 ball.",
      "claim_boundary":"One same-segment uncertainty-bound comparison only. It does not recompute the nominal residual or certify the remaining adjoint path, dual quadrature, normalizer, transfer inequality, or any continuum Navier-Stokes claim."
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    tmp=a.output.with_suffix(".tmp"); tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); tmp.replace(a.output)
    print(json.dumps(out,indent=2),flush=True)

if __name__=="__main__": main()

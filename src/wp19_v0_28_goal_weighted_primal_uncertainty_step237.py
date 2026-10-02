#!/usr/bin/env python3
"""One-segment goal-oriented bound for primal-path uncertainty.

For the frozen M14 reconstruction on step 237, integrate the linearized
primal-residual perturbation by parts in time. The volume term is the residual
of the saved adjoint Hermite polynomial against the reconstructed primal
Hermite polynomial; quadratic primal perturbations receive a separate Young
bound. This is a local diagnostic. Internal endpoint terms cancel only when
adjacent intervals are assembled with the same continuous primal error.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from flint import acb, arb, ctx
import wp19_v0_28_adjoint_segment_arb as base

ctx.prec = 192
M, STEP = 14, 237
H = arb(1) / 80000
NU = arb(1) / 10
REPORT_SHA = "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"
VALUES_SHA = "00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab"
RHS_SHA = "8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c"
SEGMENT_SHA = "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc"

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--adjoint-dir",type=Path,required=True)
    ap.add_argument("--segment",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    report=a.adjoint_dir/"M14_arb_vjp_point.json"
    if sha(report)!=REPORT_SHA: raise ValueError("frozen adjoint report mismatch")
    rec=json.loads(report.read_text())["adjoint_reconstruction"]
    values=a.adjoint_dir/rec["values_file"]
    adjrhs=a.adjoint_dir/rec["rhs_file"]
    if sha(values)!=VALUES_SHA or sha(adjrhs)!=RHS_SHA:
        raise ValueError("frozen adjoint arrays mismatch")
    if rec["values_sha256"]!=VALUES_SHA or rec["rhs_sha256"]!=RHS_SHA:
        raise ValueError("adjoint report does not bind the frozen arrays")
    if sha(a.segment)!=SEGMENT_SHA: raise ValueError("frozen step-237 segment mismatch")
    seg=json.loads(a.segment.read_text())
    if seg.get("step")!=STEP or seg.get("M")!=M or seg.get("status")!="CONTINUOUS_SEGMENT_ENCLOSURE_ONLY":
        raise ValueError("segment identity/status mismatch")

    low=base.DealiasedSystem(M,nu=.1)
    high=base.DealiasedSystem(M+1,nu=.1)
    nodes=np.load(a.lower_dir/"nodes.npy",mmap_mode="r")
    lower_rhs=np.load(a.lower_dir/"rhs.npy",mmap_mode="r")
    adj=np.load(values,mmap_mode="r")
    arhs=np.load(adjrhs,mmap_mode="r")
    for name,path in (("nodes",a.lower_dir/"nodes.npy"),
                      ("rhs",a.lower_dir/"rhs.npy"),
                      ("metadata",a.lower_dir/"metadata.json")):
        if sha(path)!=rec["lower_"+name+"_sha256"]:
            raise ValueError("frozen lower input hash mismatch: "+name)
    if nodes.shape!=(121,len(low.modes),3) or lower_rhs.shape!=nodes.shape:
        raise ValueError("lower path shape mismatch")
    if adj.shape!=(241,len(high.modes),3) or arhs.shape!=adj.shape:
        raise ValueError("adjoint path shape mismatch")

    j=STEP//2
    u_full,_=base.primal_coefficients(low,nodes,lower_rhs,j)
    u_half=base.restrict(u_full,arb(STEP%2)/2,arb(1)/2)
    u=base.embed(low,high,u_half)
    lam=base.hermite(*[base.projected_rows(high,x) for x in
                       (adj[STEP],adj[STEP+1],arhs[STEP],arhs[STEP+1])],H)

    # lambda_t - (D N(u)^* lambda + nu |k|^2 lambda), the adjoint
    # interpolation defect for F(u)=-P(u.grad)u-nu|k|^2u.
    dn_star=base.packed_vjp(high,u,lam)
    defect=[]
    for d in range(7):
        row=[]
        for i in range(len(high.modes)):
            ksq=int(high.square[i])
            vec=[]
            for c in range(3):
                lam_t=((d+1)*lam[d+1][i][c]/H if d<3 else acb(0))
                adj_rhs=dn_star[d][i][c]+(NU*ksq*lam[d][i][c] if d<4 else acb(0))
                vec.append(lam_t-adj_rhs)
            row.append(vec)
        defect.append(row)

    # Bernstein maxima bound the whole continuous time interval, not a grid.
    defect_sup=base.sup_norm(defect)
    lam_left=base.norm(lam[0])
    lam_at_right=[[sum((lam[d][i][c] for d in range(4)),acb(0)) for c in range(3)]
                  for i in range(len(high.modes))]
    lam_right=base.norm(lam_at_right)
    delta=arb(seg["bounds"]["true_primal_radius_upper"])

    # Second-order remainder: |<lambda,N(e,e)>| <= C_lambda ||e||_2^2.
    # Reuse the rigorous modewise Young coefficient for the frozen lambda
    # Hermite controls; no claim is made that this controls adjoint uncertainty.
    controls=base.bernstein(lam)
    low_mode_count=len(low.modes)
    young=arb(0)
    for b in controls:
        l1=arb(0); grad2=arb(0)
        for k,ksq,row in zip(high.modes,high.square,b):
            z=base.norm([row])
            l1+=z
            grad2+=arb(int(ksq))*z**2
        young=young.max((M*l1+arb(low_mode_count).sqrt()*grad2.sqrt()).upper()).upper()

    linear=(H*delta*defect_sup).upper()
    quadratic=(H*delta**2*young).upper()
    endpoint_local=(delta*(lam_left+lam_right)).upper()
    out={
      "schema":"wp19-v0.28-goal-weighted-primal-uncertainty-step237-v1",
      "status":"PASS_RECONSTRUCTION_ADJOINT_DEFECT_ENCLOSURE_ONLY",
      "M":M,"step":STEP,"interval_rational":["237/80000","238/80000"],
      "precision_bits":ctx.prec,
      "frozen_inputs":{"adjoint_report_sha256":sha(report),
        "adjoint_values_sha256":sha(values),"adjoint_rhs_sha256":sha(adjrhs),
        "lower_nodes_sha256":sha(a.lower_dir/"nodes.npy"),
        "lower_rhs_sha256":sha(a.lower_dir/"rhs.npy"),"segment_sha256":sha(a.segment)},
      "true_primal_radius_upper":base.safe_decimal_upper(delta,15),
      "adjoint_ode_defect_L2_sup_upper":base.safe_decimal_upper(defect_sup,12),
      "goal_weighted_linear_primal_uncertainty_integral_upper":base.safe_decimal_upper(linear,12),
      "quadratic_primal_remainder_coefficient_upper":base.safe_decimal_upper(young,12),
      "goal_weighted_quadratic_primal_remainder_integral_upper":base.safe_decimal_upper(quadratic,12),
      "local_endpoint_terms_upper":{"left":base.safe_decimal_upper(delta*lam_left,12),
        "right":base.safe_decimal_upper(delta*lam_right,12),
        "sum_if_uncancelled":base.safe_decimal_upper(endpoint_local,12)},
      "endpoint_rule":"Internal endpoint terms cancel only in a full contiguous time sum using one shared continuous primal error; this single-interval result is not a standalone signed-integral enclosure.",
      "method":"Integrate the linearized residual perturbation by parts: boundary -<lambda,e> plus <lambda_t-DN(u)^*lambda-nu|k|^2lambda,e>. Enclose the adjoint defect by Bernstein controls and the quadratic term by a frozen Fourier Young bound.",
      "claim_boundary":"This bounds only the reconstruction-based primal-uncertainty contribution on one half-step, conditional on the imported primal radius. It does not bound adjoint path uncertainty, full-time aggregation, endpoint transfer, the independent normalizer, or continuum regularity."
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2),flush=True)

if __name__=="__main__": main()

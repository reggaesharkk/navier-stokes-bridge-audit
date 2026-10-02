#!/usr/bin/env python3
"""One-segment Arb integral of reconstructed adjoint against primal defect.

This certifies the signed integral for the exact-dyadic cubic reconstructions on
one half-step only. It does not include the propagated adjoint or primal tube
radii and therefore is a quadrature preflight, not a cutoff-transfer result.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from flint import acb, arb, ctx
import wp19_v0_28_adjoint_segment_arb as base

ctx.prec = 192
M = 14
H = arb(1) / 80000
NU = arb(1) / 10
REPORT_SHA = "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"
VALUES_SHA = "00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab"
RHS_SHA = "8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c"

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def lower_decimal(x, places=15):
    upper_of_neg = base.safe_decimal_upper(-x, places)
    return upper_of_neg[1:] if upper_of_neg.startswith("-") else "-"+upper_of_neg

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--step",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--adjoint-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    n=a.step
    if not 0<=n<240:
        raise ValueError("step must lie in 0..239")
    report=a.adjoint_dir/"M14_arb_vjp_point.json"
    if sha(report)!=REPORT_SHA:
        raise ValueError("frozen M14 adjoint report mismatch")
    rec=json.loads(report.read_text())["adjoint_reconstruction"]
    values=a.adjoint_dir/rec["values_file"]
    adjrhs=a.adjoint_dir/rec["rhs_file"]
    if sha(values)!=VALUES_SHA or sha(adjrhs)!=RHS_SHA:
        raise ValueError("frozen M14 adjoint arrays mismatch")
    if rec["values_sha256"]!=VALUES_SHA or rec["rhs_sha256"]!=RHS_SHA:
        raise ValueError("adjoint report does not bind the frozen arrays")

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
            raise ValueError("lower predictor input hash mismatch: "+name)
    if nodes.shape!=(121,len(low.modes),3) or lower_rhs.shape!=nodes.shape:
        raise ValueError("lower predictor array shape mismatch")
    if adj.shape!=(241,len(high.modes),3) or arhs.shape!=adj.shape:
        raise ValueError("adjoint array shape mismatch")

    j=n//2
    u_full,_=base.primal_coefficients(low,nodes,lower_rhs,j)
    u_half=base.restrict(u_full,arb(n%2)/2,arb(1)/2)
    u=base.embed(low,high,u_half)
    lam=base.hermite(*[base.projected_rows(high,x) for x in
                       (adj[n],adj[n+1],arhs[n],arhs[n+1])],H)

    # packed_vjp(u,u) equals the projected Navier-Stokes quadratic term:
    # its first term is a gradient and vanishes under Leray projection.
    nonlinear=base.packed_vjp(high,u,u)
    residual=[]
    for d in range(7):
        row=[]
        for i in range(len(high.modes)):
            ksq=int(high.square[i])
            vec=[]
            for c in range(3):
                linear=-NU*ksq*u[d][i][c] if d<4 else acb(0)
                derivative=((d+1)*u[d+1][i][c]/H if d<3 else acb(0))
                vec.append(nonlinear[d][i][c]+linear-derivative)
            row.append(vec)
        residual.append(row)

    q=[acb(0) for _ in range(10)]
    for d in range(4):
        for e in range(7):
            term=d+e
            for i in range(len(high.modes)):
                for c in range(3):
                    q[term]+=lam[d][i][c].conjugate()*residual[e][i][c]
    integral=H*sum((q[k]/(k+1) for k in range(10)),acb(0))
    if not integral.imag.contains(0):
        raise ValueError("reconstructed real pairing has nonzero imaginary enclosure")
    value=integral.real
    out={
        "schema":"wp19-v0.28-reconstructed-dual-integral-pilot-v1",
        "status":"PASS_RECONSTRUCTION_DUAL_INTEGRAL_ONLY",
        "M":M,
        "step":n,
        "interval_rational":[f"{n}/80000",f"{n+1}/80000"],
        "precision_bits":ctx.prec,
        "frozen_inputs":{
            "adjoint_report_sha256":sha(report),
            "adjoint_values_sha256":sha(values),
            "adjoint_rhs_sha256":sha(adjrhs),
            "lower_nodes_sha256":sha(a.lower_dir/"nodes.npy"),
            "lower_rhs_sha256":sha(a.lower_dir/"rhs.npy"),
            "lower_metadata_sha256":sha(a.lower_dir/"metadata.json")
        },
        "reconstructed_signed_integral_lower":lower_decimal(value,15),
        "reconstructed_signed_integral_upper":base.safe_decimal_upper(value,15),
        "adjoint_polynomial_L2_upper":base.safe_decimal_upper(base.sup_norm(lam),12),
        "primal_defect_L2_upper":base.safe_decimal_upper(base.sup_norm(residual),12),
        "method":"Arb exact-dyadic Hermite polynomials; degree-six Fourier defect from projected quadratic convolution, viscosity and primal derivative; degree-nine signed pairing integrated coefficientwise",
        "claim_boundary":"This encloses only the signed integral for the saved reconstructions on this half-step. It does not enclose true adjoint or primal path uncertainty, the full time integral, the nonlinear remainder, endpoint Taylor remainder, or cutoff transfer."
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2),flush=True)

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Goal-weighted primal-tube uncertainty over a frozen M14 adjoint path.

Each half-step uses exact-dyadic Arb polynomial convolution. The linear
primal-path uncertainty is bounded by the adjoint ODE interpolation defect
after integration by parts; the quadratic term uses a Fourier Young bound.
Internal endpoint terms are not summed in absolute value: they telescope for
one continuous primal error across adjacent half-steps.
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

def goal_bound_for_step(low,high,nodes,lower_rhs,adj,arhs,radii,n):
    j=n//2
    if j not in goal_bound_for_step.cache:
        goal_bound_for_step.cache[j]=base.primal_coefficients(low,nodes,lower_rhs,j)
    u_full,predictor_distance=goal_bound_for_step.cache[j]
    u_half=base.restrict(u_full,arb(n%2)/2,arb(1)/2)
    u=base.embed(low,high,u_half)
    lam=base.hermite(*[base.projected_rows(high,x) for x in
                       (adj[n],adj[n+1],arhs[n],arhs[n+1])],H)

    # Saved-path adjoint ODE: lambda_t = D N(u)^*lambda + nu |k|^2 lambda.
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
    defect_sup=base.sup_norm(defect)

    delta=(radii[j]+predictor_distance).upper()
    young=arb(0)
    young_m15=arb(0)
    controls=base.bernstein(lam)
    for control in controls:
        l1=arb(0); grad2=arb(0)
        for k,ksq,mode_row in zip(high.modes,high.square,control):
            z=base.norm([mode_row])
            l1+=z
            grad2+=arb(int(ksq))*z**2
        # Re-evaluate the Fourier Young coefficient directly for M15 support,
        # rather than inflating the rounded M14 output by a global mode ratio.
        factor=(M*l1+arb(len(low.modes)).sqrt()*grad2.sqrt()).upper()
        factor_m15=((M+1)*l1+arb(len(high.modes)).sqrt()*grad2.sqrt()).upper()
        young=young.max(factor).upper()
        young_m15=young_m15.max(factor_m15).upper()
    linear=(H*delta*defect_sup).upper()
    quadratic=(H*delta**2*young).upper()
    quadratic_m15=(H*delta**2*young_m15).upper()

    if n==0:
        lam_left=base.norm(lam[0])
    else:
        lam_left=None
    if n==239:
        right=[[sum((lam[d][i][c] for d in range(4)),acb(0)) for c in range(3)]
               for i in range(len(high.modes))]
        lam_right=base.norm(right)
        terminal_primal_radius=(radii[-1]+predictor_distance).upper()
        endpoint=(lam_right*terminal_primal_radius).upper()
    else:
        lam_right=None; terminal_primal_radius=None; endpoint=None

    return {
      "step":n,"primal_segment":j,
      "true_primal_radius_upper":base.safe_decimal_upper(delta,15),
      "adjoint_ode_defect_L2_sup_upper":base.safe_decimal_upper(defect_sup,12),
      "linear_goal_integral_upper":base.safe_decimal_upper(linear,12),
      "quadratic_goal_integral_upper":base.safe_decimal_upper(quadratic,12),
      "young_M15_support_upper":base.safe_decimal_upper(young_m15,24),
      "quadratic_goal_integral_M15_support_upper":base.safe_decimal_upper(quadratic_m15,24),
      "left_endpoint_adjoint_L2_upper":base.safe_decimal_upper(lam_left,12) if lam_left is not None else None,
      "right_endpoint_adjoint_L2_upper":base.safe_decimal_upper(lam_right,12) if lam_right is not None else None,
      "terminal_primal_radius_upper":base.safe_decimal_upper(terminal_primal_radius,15) if terminal_primal_radius is not None else None,
      "terminal_endpoint_product_upper":base.safe_decimal_upper(endpoint,12) if endpoint is not None else None
    }

goal_bound_for_step.cache={}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--start",type=int,required=True)
    ap.add_argument("--count",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--adjoint-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    if a.count<=0 or a.start<0 or a.start+a.count>240:
        raise ValueError("shard must be a nonempty range inside 0..239")
    report=a.adjoint_dir/"M14_arb_vjp_point.json"
    if sha(report)!=REPORT_SHA: raise ValueError("frozen M14 adjoint report mismatch")
    rec=json.loads(report.read_text())["adjoint_reconstruction"]
    values=a.adjoint_dir/rec["values_file"]
    adjrhs=a.adjoint_dir/rec["rhs_file"]
    if sha(values)!=VALUES_SHA or sha(adjrhs)!=RHS_SHA:
        raise ValueError("frozen adjoint array hash mismatch")
    if rec.get("values_sha256")!=VALUES_SHA or rec.get("rhs_sha256")!=RHS_SHA:
        raise ValueError("adjoint report does not bind frozen arrays")
    for name,path in (("nodes",a.lower_dir/"nodes.npy"),
                      ("rhs",a.lower_dir/"rhs.npy"),
                      ("metadata",a.lower_dir/"metadata.json")):
        if sha(path)!=rec["lower_"+name+"_sha256"]:
            raise ValueError("frozen lower input hash mismatch: "+name)
    low=base.DealiasedSystem(M,nu=.1)
    high=base.DealiasedSystem(M+1,nu=.1)
    nodes=np.load(a.lower_dir/"nodes.npy",mmap_mode="r")
    lower_rhs=np.load(a.lower_dir/"rhs.npy",mmap_mode="r")
    adj=np.load(values,mmap_mode="r")
    arhs=np.load(adjrhs,mmap_mode="r")
    if nodes.shape!=(121,len(low.modes),3) or lower_rhs.shape!=nodes.shape:
        raise ValueError("lower path array shape mismatch")
    if adj.shape!=(241,len(high.modes),3) or arhs.shape!=adj.shape:
        raise ValueError("adjoint path array shape mismatch")

    radii=base.old_radius_and_identity(a.lower_dir,nodes,lower_rhs,M)
    rows=[]
    for n in range(a.start,a.start+a.count):
        rows.append(goal_bound_for_step(low,high,nodes,lower_rhs,adj,arhs,radii,n))
    out={
      "schema":"wp19-v0.28-goal-weighted-primal-tube-shard-v1",
      "status":"PASS_RECONSTRUCTION_GOAL_WEIGHTED_PRIMAL_TUBE_ONLY",
      "M":M,"start":a.start,"count":a.count,"steps":rows,
      "frozen_inputs":{"adjoint_report_sha256":sha(report),
        "adjoint_values_sha256":sha(values),"adjoint_rhs_sha256":sha(adjrhs),
        "lower_nodes_sha256":sha(a.lower_dir/"nodes.npy"),
        "lower_rhs_sha256":sha(a.lower_dir/"rhs.npy"),
        "lower_metadata_sha256":sha(a.lower_dir/"metadata.json")},
      "source_sha256":sha(Path(__file__)),
      "endpoint_rule":"Only the global endpoints survive summing by parts over a continuous primal error. Internal endpoint terms telescope and are not summed as absolute values.",
      "method":"For each interval, exact-dyadic Hermite polynomials; degree-six Arb Fourier convolution for D N(u)^* lambda; Bernstein supremum of lambda_t-D N(u)^*lambda-nu|k|^2lambda; frozen primal L2 tube radius; Fourier Young quadratic remainder.",
      "claim_boundary":"This shard bounds reconstruction-based primal-tube contributions only. It does not include terminal Taylor remainder, adjoint/input gradient uncertainty, normalizer transfer, or any continuum claim."
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"start":a.start,"count":a.count,"status":out["status"]},indent=2),flush=True)

if __name__=="__main__": main()

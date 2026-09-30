#!/usr/bin/env python3
"""WP19 v0.27c0 -- direct Arb adjoint-VJP point cross-check.

This is the arithmetic foundation for the backward-adjoint validator.  It
implements the adjoint of the dealiased quadratic Navier-Stokes nonlinearity
directly in Fourier convolution with Arb balls, using the same carry-free
polynomial encoding as the validated primal segment certificates.

The point test is deliberately interior in time so both the primal state and
adjoint have broad spectral support.  Agreement with the independent FFT
complex128 implementation is required before any whole-segment adjoint
residual certificate is attempted.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from flint import acb, acb_poly, arb, ctx

H=0.000025
NU=0.1
STEPS=120
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART="de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1"
EXPECTED_C500_SEMANTIC="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"


def ball(z):
    return acb(str(float(np.real(z))),str(float(np.imag(z))))


def point_rows(a):
    return [[ball(z) for z in row] for row in np.asarray(a)]


def project_rows(system,rows):
    out=[[acb(0) for _ in range(3)] for _ in system.modes]
    for ix,k in enumerate(system.modes):
        kk=int(system.square[ix])
        if kk==0:
            continue
        kd=sum((rows[ix][j]*int(k[j]) for j in range(3)),acb(0))
        out[ix]=[rows[ix][j]-kd*arb(int(k[j]))/kk for j in range(3)]
    return out


def carry_free_indices(system):
    base=4*system.N+1
    left=[
        (int(k[0])+system.N)
        +base*(int(k[1])+system.N)
        +base*base*(int(k[2])+system.N)
        for k in system.waves
    ]
    right=[
        (int(k[0])+2*system.N)
        +base*(int(k[1])+2*system.N)
        +base*base*(int(k[2])+2*system.N)
        for k in system.waves
    ]
    return left,right


def poly_field(rows,comp,left,n,deriv_direction=None,system=None):
    arr=[0]*n
    if deriv_direction is None:
        for ix,slot in enumerate(left):
            arr[slot]=rows[ix][comp]
    else:
        for ix,slot in enumerate(left):
            arr[slot]=rows[ix][comp]*acb(0,int(system.waves[ix,deriv_direction]))
    return acb_poly(arr)


def nonlinear_vjp_arb(system,u,lam):
    """Arb Fourier form of v23.nonlinear_vjp.

    q_j = sum_i lambda_i * partial_j u_i
          - sum_i u_i * partial_i lambda_j,
    followed by Leray projection at the output mode.
    """
    u=project_rows(system,u)
    lam=project_rows(system,lam)
    left,right=carry_free_indices(system)
    n=max(left)+1

    U=[poly_field(u,i,left,n) for i in range(3)]
    L=[poly_field(lam,i,left,n) for i in range(3)]

    q=[[acb(0) for _ in range(3)] for _ in system.modes]
    for j in range(3):
        first=None
        for i in range(3):
            du=poly_field(u,i,left,n,deriv_direction=j,system=system)
            prod=L[i]*du
            first=prod if first is None else first+prod
        second=None
        for i in range(3):
            dl=poly_field(lam,j,left,n,deriv_direction=i,system=system)
            prod=U[i]*dl
            second=prod if second is None else second+prod
        for ix,slot in enumerate(right):
            q[ix][j]=first[slot]-second[slot]

    return project_rows(system,q)


def l2_upper(rows):
    s=arb(0)
    for row in rows:
        for z in row:
            u=z.abs_upper()
            s+=u*u
    return s.sqrt().upper()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--M",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--sign-chart",type=Path,required=True)
    ap.add_argument("--c500",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    if args.M not in (14,15,16,17):
        raise ValueError("supported M are 14,15,16,17")

    root=args.repo.resolve()
    sys.path.insert(0,str((root/"src").resolve()))
    sys.path.insert(0,str((root/"next-work"/"n14_same_datum"/"tools").resolve()))
    import wp19_v0_23_rk4_goal_adjoint as v23
    import wp19_v0_26_signed_goal_adjoint as v26
    import wp19_v0_27_terminal_gradient_arb as v27a
    import arb_common_n14 as common
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    if v26.sha256(args.sign_chart)!=EXPECTED_SIGN_CHART:
        raise ValueError("sign chart hash mismatch")
    coeff,_,_,sem=v26.load_coefficients(args.sign_chart,args.c500)
    if sem!=EXPECTED_C500_SEMANTIC:
        raise ValueError("C500 semantic mismatch")

    M=args.M
    low=DealiasedSystem(M,nu=NU)
    high=DealiasedSystem(M+1,nu=NU)
    fixed=DealiasedSystem(11,nu=NU)
    meta=json.loads((args.lower_dir/"metadata.json").read_text())
    if (
        meta.get("N")!=M
        or meta.get("witness_sha256")!=EXPECTED_WITNESS
        or meta.get("K36_keys_sha256")!=EXPECTED_K36
    ):
        raise ValueError("lower predictor metadata mismatch")

    lo_nodes=np.load(args.lower_dir/"nodes.npy",mmap_mode="r")
    lo_rhs=np.load(args.lower_dir/"rhs.npy",mmap_mode="r")
    idx11=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    base11=v23.physical_project(fixed,np.asarray(lo_nodes[-1,idx11]))
    _,grad11=v26.torch_terminal_gradient(fixed,base11,coeff,v23.tangent_project)

    high_idx11=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    lam=np.zeros((len(high.modes),3),dtype=np.complex128)
    lam[high_idx11]=grad11
    lambdas=[None]*(2*STEPS+1)
    lambdas[-1]=lam.copy()

    def segval(j,theta):
        return v26.segment_value(v23,lo_nodes,lo_rhs,j,theta)
    def x_at(j,theta):
        return v23.embed(low,high,segval(j,theta))

    dt=-H/2.0
    for j in range(STEPS-1,-1,-1):
        for sub in (1,0):
            theta1=(sub+1)/2.0
            theta0=sub/2.0
            thetam=0.5*(theta0+theta1)
            u1=x_at(j,theta1)
            um=x_at(j,thetam)
            u0=x_at(j,theta0)
            k1=v23.adjoint_rhs(high,u1,lam)
            k2=v23.adjoint_rhs(high,um,lam+0.5*dt*k1)
            k3=v23.adjoint_rhs(high,um,lam+0.5*dt*k2)
            k4=v23.adjoint_rhs(high,u0,lam+dt*k3)
            lam=lam+(dt/6.0)*(k1+2*k2+2*k3+k4)
            lam=v23.physical_project(high,lam)
            lambdas[2*j+sub]=lam.copy()

    # Interior original node j=60, t=T/2.
    j=60
    n=2*j
    u_float=v23.embed(low,high,np.asarray(lo_nodes[j]))
    lam_float=np.asarray(lambdas[n])
    ref=v23.nonlinear_vjp(high,u_float,lam_float)

    ctx.prec=192
    got=nonlinear_vjp_arb(high,point_rows(u_float),point_rows(lam_float))

    diff=[]
    for ix in range(len(high.modes)):
        diff.append([got[ix][c]-ball(ref[ix,c]) for c in range(3)])
    diff_upper=l2_upper(diff)
    ref_norm=float(np.linalg.norm(ref.ravel()))
    rel=(diff_upper/arb(str(max(1.0,ref_norm)))).upper()

    if rel>arb("1e-10"):
        raise ValueError(("Arb/direct VJP vs FFT discrepancy too large",str(rel)))

    out={
        "schema":"wp19-v0.27c0-arb-adjoint-vjp-point-crosscheck-v1",
        "status":"PASS ARB ADJOINT-VJP POINT CROSSCHECK",
        "M":M,
        "transition":f"{M}->{M+1}",
        "test_node":j,
        "test_time_decimal":"0.0015",
        "arb_precision_bits":ctx.prec,
        "frozen":{
            "witness_sha256":EXPECTED_WITNESS,
            "K36_sha256":EXPECTED_K36,
            "K36_sign_chart_sha256":EXPECTED_SIGN_CHART,
            "C500_portable_semantic_sha256":sem,
        },
        "reference_fft_vjp_L2":ref_norm,
        "arb_vs_fft_L2_difference_upper_decimal":common.decimal_upper(diff_upper,9),
        "arb_vs_fft_relative_difference_upper_decimal":common.decimal_upper(rel,15),
        "method":"Direct carry-free Arb convolution of q_j=sum_i lambda_i partial_j u_i - sum_i u_i partial_i lambda_j, followed by the Leray projection; compared at an interior broad-support state against the independent dealiased FFT VJP.",
        "next_target":"Use this Arb VJP kernel inside a whole-segment polynomial residual enclosure for the backward adjoint.",
        "claim_boundary":"Arithmetic cross-check of the adjoint nonlinear operator at one interior point only; not yet an adjoint trajectory certificate and no all-N/continuum claim.",
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""WP19 v0.26 fixed signed-C500 numerator Hermite goal-adjoint scout.

Floating route-selection and intervalization-design stage only.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np

H=0.000025
NU=0.1
STEPS=120
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_C500_SEMANTIC="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"

def cert_check(path:Path,N:int,kkeys,sig):
    x=json.loads(path.read_text())
    if x.get("N")!=N or x.get("status")!="PASS":
        raise ValueError(f"bad endpoint certificate N{N}")
    if x.get("C500_semantic_sha256")!=EXPECTED_C500_SEMANTIC:
        raise ValueError("C500 semantic mismatch in endpoint certificate")
    rows=x.get("K36_sign_rows",[])
    if len(rows)!=36: raise ValueError("K36 sign-row count mismatch")
    cmap={(tuple(r["left_orbit"]),tuple(r["right_orbit"])):(int(r["sign"]),bool(r["locked"])) for r in rows}
    for key,s in zip(kkeys,sig):
        if key not in cmap or cmap[key]!=(int(s),True):
            raise ValueError(f"frozen K36 sign mismatch at N{N}: {key}")
    return x

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--M",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--higher-dir",type=Path,required=True)
    ap.add_argument("--k36",type=Path,required=True)
    ap.add_argument("--sign-chart",type=Path,required=True)
    ap.add_argument("--c500",type=Path,required=True)
    ap.add_argument("--lower-cert",type=Path,required=True)
    ap.add_argument("--higher-cert",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()

    sys.path.insert(0,str((a.repo/"src").resolve()))
    import wp19_v0_23_rk4_goal_adjoint as v23
    import wp19_v0_24_hermite_goal_remainder as v24
    import wp19_v0_26_signed_objective as obj
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    M=a.M
    if M not in (14,15,16,17):
        raise ValueError("frozen v0.26 transition must be 14->15 through 17->18")
    low=DealiasedSystem(M,nu=NU);high=DealiasedSystem(M+1,nu=NU);fixed=DealiasedSystem(11,nu=NU)
    kkeys,sig,ckeys,tau=obj.load_frozen(a.k36,a.sign_chart,a.c500)

    for d,N in ((a.lower_dir,M),(a.higher_dir,M+1)):
        meta=json.loads((d/"metadata.json").read_text())
        if meta["N"]!=N or meta["witness_sha256"]!=EXPECTED_WITNESS or meta["K36_keys_sha256"]!=EXPECTED_K36:
            raise ValueError("predictor metadata mismatch")

    clo=cert_check(a.lower_cert,M,kkeys,sig);chi=cert_check(a.higher_cert,M+1,kkeys,sig)
    lo_nodes=np.load(a.lower_dir/"nodes.npy",mmap_mode="r");lo_rhs=np.load(a.lower_dir/"rhs.npy",mmap_mode="r")
    hi_nodes=np.load(a.higher_dir/"nodes.npy",mmap_mode="r");hi_rhs=np.load(a.higher_dir/"rhs.npy",mmap_mode="r")
    if len(lo_nodes)!=STEPS+1 or len(hi_nodes)!=STEPS+1: raise ValueError("node count mismatch")

    il=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    ih=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    base=v23.physical_project(fixed,np.asarray(lo_nodes[-1,il]))
    target=v23.physical_project(fixed,np.asarray(hi_nodes[-1,ih]))
    J0,nk0,_,_=obj.numpy_objective(fixed,base,kkeys,sig,ckeys,tau)
    J1,nk1,_,_=obj.numpy_objective(fixed,target,kkeys,sig,ckeys,tau)
    Jt,graw=obj.torch_gradient(fixed,base,kkeys,sig,ckeys,tau)
    grad=v23.tangent_project(fixed,graw)
    if abs(Jt-J0)>2e-9*max(1.0,abs(J0)): raise ValueError(("torch/numpy objective mismatch",Jt,J0))
    if np.any(np.sign(nk0)!=sig) or np.any(np.sign(nk1)!=sig): raise ValueError("floating endpoint exits frozen sign chamber")

    ex0=float(clo["nominal_signed_numerator_decimal"]);ex1=float(chi["nominal_signed_numerator_decimal"])
    for label,x,y in (("base",J0,ex0),("target",J1,ex1)):
        rel=abs(x-y)/max(1.0,abs(y))
        if rel>5e-11: raise ValueError((label,"floating/exact nominal mismatch",x,y,rel))

    delta=target-base; actual=float(J1-J0)
    endpoint_linear=float(np.real(np.vdot(grad.ravel(),delta.ravel())))
    endpoint_rem=float(actual-endpoint_linear)
    eT=float(np.linalg.norm(delta.ravel()))
    direction=delta/eT
    eps=1e-8
    fp=obj.numpy_objective(fixed,v23.physical_project(fixed,base+eps*direction),kkeys,sig,ckeys,tau)[0]
    fm=obj.numpy_objective(fixed,v23.physical_project(fixed,base-eps*direction),kkeys,sig,ckeys,tau)[0]
    fd=(fp-fm)/(2*eps);ad=float(np.real(np.vdot(grad.ravel(),direction.ravel())))
    grad_rel=abs(fd-ad)/max(1.0,abs(fd),abs(ad))
    if grad_rel>2e-5: raise ValueError(("objective gradient check failed",fd,ad,grad_rel))

    high_i11=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    lam=np.zeros((len(high.modes),3),dtype=np.complex128);lam[high_i11]=grad
    terminal_norm=float(np.linalg.norm(lam.ravel()))
    lambdas=[None]*(2*STEPS+1);lambdas[-1]=lam.copy()

    def xat(j,t):
        return v23.embed(low,high,v24.segment_value(v23,lo_nodes,lo_rhs,j,t))

    dt=-H/2.0
    for j in range(STEPS-1,-1,-1):
        for sub in (1,0):
            t1=(sub+1)/2.0;t0=sub/2.0;tm=0.5*(t0+t1)
            u1=xat(j,t1);um=xat(j,tm);u0=xat(j,t0)
            k1=v23.adjoint_rhs(high,u1,lam);k2=v23.adjoint_rhs(high,um,lam+0.5*dt*k1)
            k3=v23.adjoint_rhs(high,um,lam+0.5*dt*k2);k4=v23.adjoint_rhs(high,u0,lam+dt*k3)
            lam=lam+(dt/6.0)*(k1+2*k2+2*k3+k4);lam=v23.physical_project(high,lam)
            lambdas[2*j+sub]=lam.copy()
        if j%20==0: print("M",M,"signed-numerator adjoint segment",j,flush=True)

    elo=v24.halfgrid_error_schedule(a.lower_dir);ehi=v24.halfgrid_error_schedule(a.higher_dir)
    dual=np.empty(2*STEPS+1);rnorm=np.empty_like(dual);gl1=np.empty_like(dual);enom=np.empty_like(dual);eup=np.empty_like(dual)
    for n in range(2*STEPS+1):
        if n==2*STEPS: j=STEPS-1;t=1.0
        else: j=n//2;t=0.0 if n%2==0 else 0.5
        lo=v24.segment_value(v23,lo_nodes,lo_rhs,j,t)
        lodot=v24.hermite_derivative(np.asarray(lo_nodes[j]),np.asarray(lo_nodes[j+1]),np.asarray(lo_rhs[j]),np.asarray(lo_rhs[j+1]),t)
        hi=v24.segment_value(v23,hi_nodes,hi_rhs,j,t)
        x=v23.embed(low,high,lo);xdot=v23.embed(low,high,lodot);r=high.rhs(x)-xdot;e=np.asarray(hi)-x
        rnorm[n]=float(np.linalg.norm(r.ravel()));dual[n]=float(np.real(np.vdot(lambdas[n].ravel(),r.ravel())))
        gl1[n]=v24.grad_fourier_l1(high,lambdas[n]);enom[n]=float(np.linalg.norm(e.ravel()));eup[n]=enom[n]+elo[n]+ehi[n]

    eta=v24.simpson(dual);dyn=float(endpoint_linear-eta)
    nl_nom=v24.simpson(gl1*enom*enom);nl_rad=v24.simpson(gl1*eup*eup)
    up0=float(clo["true_signed_numerator_upper_decimal"]);up1=float(chi["true_signed_numerator_upper_decimal"])
    margin0=-up0;margin1=-up1
    if margin0<=0 or margin1<=0: raise ValueError("endpoint certified margin not negative")

    out={
      "schema":"wp19-v0.26-signed-c500-numerator-goal-adjoint-v1",
      "copyright":"Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
      "status":"PASS FLOATING SIGNED-NUMERATOR ROUTE GATE",
      "transition":f"{M}->{M+1}",
      "objective":"fixed degree-7 polynomial signed-C500 numerator on P11",
      "frozen":{
        "witness_sha256":EXPECTED_WITNESS,"K36_sha256":EXPECTED_K36,
        "K36_sign_chart_sha256":obj.EXPECTED_SIGN_CHART,"C500_semantic_sha256":EXPECTED_C500_SEMANTIC,
        "K36_signs_retuned":False,"C500_retuned":False},
      "base_nominal_signed_numerator":J0,"target_nominal_signed_numerator":J1,"actual_delta_signed_numerator":actual,
      "exact_endpoint_crosscheck":{
        "base_exact_nominal":ex0,"target_exact_nominal":ex1,"base_certified_upper":up0,"target_certified_upper":up1,
        "base_negative_margin":margin0,"target_negative_margin":margin1,
        "all_36_frozen_signs_match_both_certified_endpoints":True},
      "endpoint_gradient_linear_prediction":endpoint_linear,"endpoint_taylor_remainder_observed":endpoint_rem,
      "endpoint_nominal_difference_L2":eT,
      "observed_directional_curvature_2R_over_e2":2*abs(endpoint_rem)/(eT*eT),
      "objective_gradient_directional_check_relative_error":grad_rel,
      "terminal_adjoint_norm":terminal_norm,"initial_adjoint_norm":float(np.linalg.norm(lambdas[0].ravel())),
      "hermite_simpson_dual_prediction":eta,"total_remainder_actual_minus_dual":float(actual-eta),
      "total_relative_remainder":abs(actual-eta)/max(abs(actual),1e-30),
      "dynamic_remainder_endpoint_linear_minus_dual":dyn,
      "full_reconstruction_residual_max_L2":float(rnorm.max()),
      "adjoint_gradient_fourier_l1_max":float(gl1.max()),
      "adjoint_gradient_fourier_l1_simpson_integral":v24.simpson(gl1),
      "state_difference":{
        "nominal_max_halfgrid_L2":float(enom.max()),"radius_augmented_max_halfgrid_L2_scout":float(eup.max()),
        "nominal_endpoint_L2":float(enom[-1]),"radius_augmented_endpoint_L2_scout":float(eup[-1])},
      "nonlinear_dynamic_remainder_candidate":{
        "identity_bound":"|<lambda,B(e,e)>| <= ||grad lambda||_infty ||e||_2^2",
        "nominal_simpson_bound":nl_nom,"radius_augmented_simpson_bound_scout":nl_rad,
        "observed_abs_dynamic_remainder":abs(dyn),"radius_bound_over_observed":nl_rad/max(abs(dyn),1e-30)},
      "margin_ratios":{
        "abs_actual_delta_over_base_certified_margin":abs(actual)/margin0,
        "abs_dual_prediction_over_base_certified_margin":abs(eta)/margin0,
        "abs_total_remainder_over_base_certified_margin":abs(actual-eta)/margin0,
        "radius_nonlinear_bound_over_base_certified_margin":nl_rad/margin0},
      "method":"Frozen-sign signed numerator; projected PyTorch terminal gradient; half-step RK4 continuous adjoint along cubic-Hermite lower reconstruction; full Hermite residual; Simpson pairing; binary64 replay of rigorous trajectory radii; exact v0.25b endpoint sign/margin cross-check.",
      "claim_boundary":"Floating transfer/intervalization-design gate only. No terminal-gradient, adjoint, quadrature, endpoint-Hessian, or nonlinear-remainder interval enclosure is claimed; no all-N or continuum theorem."
    }
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"transition":out["transition"],"actual":actual,"dual":eta,"relative_remainder":out["total_relative_remainder"],"gradient_check_rel":grad_rel,"base_margin":margin0,"dual_over_margin":out["margin_ratios"]["abs_dual_prediction_over_base_certified_margin"],"radius_bound_over_margin":out["margin_ratios"]["radius_nonlinear_bound_over_base_certified_margin"]},indent=2))

if __name__=="__main__":
    main()

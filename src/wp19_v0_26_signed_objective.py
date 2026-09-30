#!/usr/bin/env python3
"""Frozen smooth signed-C500 numerator used by WP19 v0.26.

The objective is the unnormalised polynomial numerator
  J = sum_{g in K36} sigma_g n_g - 9 sum_{g in C500} tau_g n_g,
with sigma frozen by the prospective N13 sign chart and tau frozen by C500.
"""
from __future__ import annotations
import hashlib,json
from collections import defaultdict
from pathlib import Path
import numpy as np

P,Q,K=(3,2,2),(3,-2,1),(6,0,3)
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART="7cbb307c70aa14fabdc28ae07f0965716bf498e63c371b61e1b9bfd00611c7bd"
EXPECTED_C500_SEMANTIC="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def c500_semantic_sha(path:Path):
    obj=json.loads(path.read_text())
    semantic={
        "schema":"wp19-c500-semantic-identity-v1",
        "coalition_size":int(obj["coalition_size"]),
        "keys":[{
            "rank":int(r["rank_from_N11_endpoint"]),
            "left_orbit":[int(x) for x in r["left_orbit"]],
            "right_orbit":[int(x) for x in r["right_orbit"]],
            "fixed_linear_sign":int(r["fixed_linear_sign"]),
        } for r in obj["keys"]],
    }
    raw=(json.dumps(semantic,sort_keys=True,separators=(",",":"))+"\n").encode()
    return hashlib.sha256(raw).hexdigest()

def load_frozen(k36_path:Path,sign_path:Path,c500_path:Path):
    if hashlib.sha256(k36_path.read_bytes()).hexdigest()!=EXPECTED_K36:
        raise ValueError("K36 hash mismatch")
    if hashlib.sha256(sign_path.read_bytes()).hexdigest()!=EXPECTED_SIGN_CHART:
        raise ValueError("K36 sign-chart hash mismatch")
    if c500_semantic_sha(c500_path)!=EXPECTED_C500_SEMANTIC:
        raise ValueError("C500 semantic hash mismatch")
    krows=json.loads(k36_path.read_text())["keys"]
    srows=json.loads(sign_path.read_text())["keys"]
    crows=json.loads(c500_path.read_text())["keys"]
    if (len(krows),len(srows),len(crows))!=(36,36,500):
        raise ValueError("frozen object size mismatch")
    kkeys=[(tuple(r["left_orbit"]),tuple(r["right_orbit"])) for r in krows]
    smap={(tuple(r["left_orbit"]),tuple(r["right_orbit"])):int(r["fixed_numerator_sign"]) for r in srows}
    if set(kkeys)!=set(smap):
        raise ValueError("sign chart/key mismatch")
    sig=np.asarray([smap[k] for k in kkeys],float)
    ckeys=[(tuple(r["left_orbit"]),tuple(r["right_orbit"])) for r in crows]
    tau=np.asarray([int(r["fixed_linear_sign"]) for r in crows],float)
    if set(kkeys)&set(ckeys) or not np.all(np.isin(sig,[-1,1])) or not np.all(np.isin(tau,[-1,1])):
        raise ValueError("invalid frozen signs/overlap")
    return kkeys,sig,ckeys,tau

def numpy_objective(system,a,kkeys,sig,ckeys,tau):
    a=np.asarray(a,np.complex128)
    pi,qi,ki=(system.index[x] for x in (P,Q,K))
    Pk=system.projectors[ki]; W=float(system.square[ki]**2)
    b=Pk@(1j*np.dot(np.asarray(Q,float),a[pi])*a[qi])
    z=-W*np.vdot(a[ki],b)
    wanted=set(kkeys)|set(ckeys); groups=defaultdict(complex)
    for l0,r0 in zip(system.left,system.right):
        l=int(l0); r=int(r0); key=(orbit(system.modes[l]),orbit(system.modes[r]))
        if key not in wanted: continue
        d=-(Pk@(1j*np.dot(system.waves[r],a[l])*a[r]))
        groups[key]+=-W*np.vdot(d,b)
    nk=np.asarray([np.imag(groups[k]*np.conj(z)) for k in kkeys],float)
    nc=np.asarray([np.imag(groups[k]*np.conj(z)) for k in ckeys],float)
    return float(np.dot(sig,nk)-9.0*np.dot(tau,nc)),nk,nc,z

def torch_gradient(system,a_np,kkeys,sig,ckeys,tau):
    import torch
    torch.set_default_dtype(torch.float64)
    keys=kkeys+ckeys; gid={k:i for i,k in enumerate(keys)}
    li=[];ri=[];waves=[];gids=[]
    for l0,r0 in zip(system.left,system.right):
        l=int(l0);r=int(r0);key=(orbit(system.modes[l]),orbit(system.modes[r]))
        if key in gid:
            li.append(l);ri.append(r);waves.append(system.waves[r]);gids.append(gid[key])
    a=torch.tensor(np.asarray(a_np),dtype=torch.complex128,requires_grad=True)
    li=torch.tensor(li,dtype=torch.long);ri=torch.tensor(ri,dtype=torch.long)
    waves=torch.tensor(np.asarray(waves),dtype=torch.float64).to(torch.complex128)
    gids=torch.tensor(gids,dtype=torch.long)
    Pk=torch.tensor(system.projectors[system.index[K]],dtype=torch.float64).to(torch.complex128)
    q=torch.tensor(Q,dtype=torch.float64).to(torch.complex128)
    kv=torch.tensor(K,dtype=torch.float64).to(torch.complex128);k2=float(sum(x*x for x in K))
    pi,qi,ki=(system.index[x] for x in (P,Q,K));W=float(system.square[ki]**2)
    b=Pk@(1j*torch.sum(q*a[pi])*a[qi]);z=-W*torch.vdot(a[ki],b)
    raw=1j*torch.sum(waves*a[li],dim=-1)[:,None]*a[ri]
    kd=torch.sum(raw*kv[None,:],dim=-1);d=-(raw-kd[:,None]*kv[None,:]/k2)
    grouped=torch.zeros((len(keys),3),dtype=torch.complex128).index_add(0,gids,d)
    w=-W*torch.sum(torch.conj(grouped)*b[None,:],dim=-1)
    n=torch.imag(w*torch.conj(z))
    J=torch.sum(torch.tensor(sig,dtype=torch.float64)*n[:len(kkeys)])-9.0*torch.sum(torch.tensor(tau,dtype=torch.float64)*n[len(kkeys):])
    J.backward()
    return float(J.detach().cpu().numpy()),a.grad.detach().cpu().numpy()

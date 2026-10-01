#!/usr/bin/env python3
"""Independent Bernstein recheck of the M14 segment-237 strain upper only.

This module does not import the segment producer. It reconstructs the frozen
low-cutoff Hermite field from the archived NumPy arrays as exact dyadic points,
reconstructs the decimal-projected centre as exact decimal points, and
independently encloses the cubic Bernstein strain supremum and centre
mismatch. It does not re-evaluate the nonlinear adjoint residual.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
from flint import acb, arb, ctx

M = 14
STEP = 237
PRIMAL_SEGMENT = 118
H = arb(1) / 40000
HALF_H = arb(1) / 80000
EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36 = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_NODES = "e0b0a36d8b308cccb5befb3abe45777ec0775cbc7e5a76fef0011eed0fd1f7f0"
EXPECTED_RHS = "f3a55190e9cba625b7285e5ba3e09e68fa4027e7a8909d1ad80671c1ee1ef253"
EXPECTED_SOURCE = "e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31"
EXPECTED_FROZEN = {
    "witness_sha256": EXPECTED_WITNESS,
    "K36_sha256": EXPECTED_K36,
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""): h.update(block)
    return h.hexdigest()

def safe_decimal_upper(x: arb, places: int) -> str:
    mid,rad,exp=(int(v) for v in x.mid_rad_10exp())
    n=mid+rad
    shift=exp+places
    if shift>=0:
        grid=n*10**shift
        units=grid
    else:
        den=10**(-shift)
        grid=n
        units=-((-n)//den)
    units+=1
    if shift>=0:
        above=units>grid
    else:
        above=units*den>grid
    if not above: raise ArithmeticError("outward decimal formatting failed")
    sign="-" if units<0 else ""
    digits=str(abs(units)).zfill(places+1)
    if places: digits=digits[:-places]+"."+digits[-places:]
    return sign+digits

def modes(cutoff: int):
    out=[]
    for x in range(-cutoff,cutoff+1):
        for y in range(-cutoff,cutoff+1):
            for z in range(-cutoff,cutoff+1):
                sq=x*x+y*y+z*z
                if sq<=cutoff*cutoff: out.append(((x,y,z),sq))
    return out

def dyadic_complex(z) -> acb:
    z=complex(z)
    rn,rd=z.real.as_integer_ratio(); imn,imd=z.imag.as_integer_ratio()
    return acb(arb(rn)/rd,arb(imn)/imd)

def decimal_complex(z) -> acb:
    z=complex(z)
    return acb(str(float(z.real)),str(float(z.imag)))

def project(system_modes, array, importer):
    out=[[acb(0) for _ in range(3)] for _ in system_modes]
    pos={k:i for i,(k,_) in enumerate(system_modes)}
    for ix,(k,sq) in enumerate(system_modes):
        if k <= tuple(-v for v in k): continue
        raw=[importer(z) for z in array[ix]]
        if sq:
            kd=sum((raw[j]*k[j] for j in range(3)),acb(0))
            trans=[raw[j]-kd*k[j]/sq for j in range(3)]
        else: trans=[acb(0)]*3
        out[ix]=trans
        out[pos[tuple(-v for v in k)]]=[v.conjugate() for v in trans]
    return out

def hermite(a,b,f,g,h):
    return [a,
      [[h*z for z in row] for row in f],
      [[3*(b[i][j]-a[i][j])-h*(2*f[i][j]+g[i][j]) for j in range(3)] for i in range(len(a))],
      [[2*(a[i][j]-b[i][j])+h*(f[i][j]+g[i][j]) for j in range(3)] for i in range(len(a))]]

def restrict(c,start,width):
    return [[[sum((c[d][i][j]*math.comb(d,r)*start**(d-r)*width**r for d in range(r,4)),acb(0))
              for j in range(3)] for i in range(len(c[0]))] for r in range(4)]

def bernstein(c):
    degree=len(c)-1
    return [[[sum((c[d][i][t]*math.comb(j,d)/math.comb(degree,d) for d in range(j+1)),acb(0))
              for t in range(3)] for i in range(len(c[0]))] for j in range(degree+1)]

def l2_upper(rows):
    total=arb(0)
    for row in rows:
        for z in row:
            a=z.abs_upper(); total+=a*a
    return total.sqrt().upper()

def coefficient_mismatch(c):
    return max((l2_upper(b) for b in bernstein(c)),default=arb(0)).upper()

def strain_sup(system_modes,c):
    best=arb(0)
    invsqrt2=arb(2).sqrt().inv()
    for control in bernstein(c):
        total=arb(0)
        for (k,sq),row in zip(system_modes,control):
            total+=arb(sq).sqrt()*l2_upper([row])*invsqrt2
        best=best.max(total).upper()
    return best

def primal_radius(lower_dir,nodes,rhs):
    metadata=json.loads((lower_dir/"metadata.json").read_text())
    if metadata.get("N")!=M or metadata.get("steps")!=120 or metadata.get("h_exact_decimal")!="0.000025" or metadata.get("initial_error_bound_decimal")!="0":
        raise ValueError("frozen N14 lower-certificate metadata mismatch")
    if metadata.get("witness_sha256")!=EXPECTED_WITNESS or metadata.get("K36_keys_sha256")!=EXPECTED_K36:
        raise ValueError("frozen witness/K36 identity mismatch")
    if sha(lower_dir/"nodes.npy")!=metadata.get("nodes_sha256") or sha(lower_dir/"rhs.npy")!=metadata.get("rhs_sha256"):
        raise ValueError("lower-array hash mismatch")
    E=arb(0); radii=[]
    for j in range(120):
        row=json.loads((lower_dir/f"{j:03d}.json").read_text())
        digest=hashlib.sha256(b"".join(x.tobytes() for x in (nodes[j],nodes[j+1],rhs[j],rhs[j+1]))).hexdigest()
        if row.get("step")!=j or row.get("input_binary_sha256")!=digest:
            raise ValueError(("lower segment identity mismatch",j))
        if j==0 and row.get("exact_rational_initial_field_sha256")!=EXPECTED_WITNESS:
            raise ValueError("initial exact-rational field identity mismatch")
        R=arb(row["residual_L2_upper_decimal"])
        G=arb(row["gradient_Fourier_l1_upper_decimal"])
        if not R>=0 or not G>=0: raise ValueError(("negative lower bound",j))
        # Preserve the archived outward recurrence and its 12-place grid.
        E=arb(safe_decimal_upper((G*H).exp()*(E+H*R),12))
        radii.append(E)
    return radii

def run(lower_dir: Path, segment_path: Path):
    ctx.prec=192
    segment=json.loads(segment_path.read_text())
    if sha(segment_path)!="c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc":
        raise ValueError("segment-237 output identity mismatch")
    if segment.get("M")!=M or segment.get("step")!=STEP or segment.get("frozen")!=EXPECTED_FROZEN:
        raise ValueError("segment-237 frozen scope mismatch")
    if segment.get("source_sha256")!=EXPECTED_SOURCE or segment.get("status")!="CONTINUOUS_SEGMENT_ENCLOSURE_ONLY":
        raise ValueError("segment producer/status mismatch")
    nodes=np.load(lower_dir/"nodes.npy",mmap_mode="r")
    rhs=np.load(lower_dir/"rhs.npy",mmap_mode="r")
    if nodes.shape!=(121,11513,3) or rhs.shape!=nodes.shape: raise ValueError("lower array shape mismatch")
    if sha(lower_dir/"nodes.npy")!=EXPECTED_NODES or sha(lower_dir/"rhs.npy")!=EXPECTED_RHS:
        raise ValueError("lower predictor hashes differ from frozen segment")
    system=modes(M)
    if len(system)!=11513 or sum(sq for _,sq in system)!=1355442:
        raise ValueError("independent Fourier-ball enumeration mismatch")
    j=PRIMAL_SEGMENT
    dyadic=[project(system,a,dyadic_complex) for a in (nodes[j],nodes[j+1],rhs[j],rhs[j+1])]
    decimal=[project(system,a,decimal_complex) for a in (nodes[j],nodes[j+1],rhs[j],rhs[j+1])]
    u_dyadic=hermite(*dyadic,H)
    u_decimal=hermite(*decimal,H)
    diff=[[[u_dyadic[d][i][t]-u_decimal[d][i][t] for t in range(3)] for i in range(len(system))] for d in range(4)]
    centre_gap=coefficient_mismatch(diff)
    half=restrict(u_dyadic,arb(1)/2,arb(1)/2)
    radii=primal_radius(lower_dir,nodes,rhs)
    radius=(radii[j]+centre_gap).upper()
    ksq=sum(sq for _,sq in system)
    uncertainty=(arb(ksq)/2).sqrt()*radius
    nominal=strain_sup(system,half)
    total=(nominal+uncertainty).upper()
    logged=arb(segment["bounds"]["logarithmic_norm_upper"])
    if total>logged: raise ValueError("independent strain upper exceeds archived strain upper")
    return {
      "schema":"wp19-v0.28-independent-strain-bernstein-check-v1",
      "status":"PASS_INDEPENDENT_STRAIN_BERNSTEIN_ONLY",
      "M":M,"step":STEP,"primal_segment":PRIMAL_SEGMENT,"precision_bits":ctx.prec,
      "segment_sha256":sha(segment_path),"lower_nodes_sha256":sha(lower_dir/"nodes.npy"),"lower_rhs_sha256":sha(lower_dir/"rhs.npy"),
      "frozen":EXPECTED_FROZEN,
      "independent_mode_count":len(system),"sum_squared_wave_numbers":ksq,
      "dyadic_decimal_centre_gap_upper":safe_decimal_upper(centre_gap,18),
      "archived_primal_radius_before_centre_gap":safe_decimal_upper(radii[j],18),
      "true_primal_radius_upper":safe_decimal_upper(radius,15),
      "nominal_strain_bernstein_upper":safe_decimal_upper(nominal,12),
      "strain_uncertainty_upper":safe_decimal_upper(uncertainty,12),
      "independent_total_strain_upper":safe_decimal_upper(total,12),
      "archived_logarithmic_norm_upper":segment["bounds"]["logarithmic_norm_upper"],
      "archived_upper_dominates_independent_reconstruction":True,
      "scope":{"checked":["frozen identities","exact-dyadic and decimal-centre reconstruction","lower trajectory recurrence","whole-half-segment Bernstein strain upper"],
               "not_checked":["nonlinear adjoint residual convolution","full adjoint path","dual quadrature","nonlinear remainder","normalizer","endpoint transfer","continuum regularity"]}
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-check",action="store_true")
    p.add_argument("--lower-dir",type=Path)
    p.add_argument("--segment",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_check:
        ctx.prec=192
        # Verify cubic coordinate substitution, restriction, and Bernstein hull.
        c=[[[acb(v),acb(0),acb(0)]] for v in (1,2,3,4)]
        q=restrict(c,arb(1)/2,arb(1)/2)
        expected=["3.25","4","2.25","0.5"]
        if any(not q[i][0][0].real.overlaps(arb(expected[i])) for i in range(4)):
            raise ValueError("cubic half-step restriction self-check failed")
        controls=bernstein(q)
        control_values=[("3.25","55/12","20/3","10")]
        if any(not controls[j][0][0].real.overlaps(arb(control_values[0][j])) for j in range(4)):
            raise ValueError("cubic Bernstein-control self-check failed")
        constant=[[[acb(2),acb(0),acb(0)]]]
        if bernstein(constant)[0][0][0]!=acb(2): raise ValueError("Bernstein constant self-check failed")
        x=arb("1234567890123.000001")
        if Fraction(safe_decimal_upper(x,6))<=Fraction(1234567890123000001,1000000):
            raise ValueError("outward-decimal self-check failed")
        print("PASS independent strain checker helper self-check")
        return
    if any(x is None for x in (a.lower_dir,a.segment,a.output)): p.error("--lower-dir, --segment, and --output are required")
    result=run(a.lower_dir,a.segment)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2),flush=True)
if __name__=="__main__": main()
